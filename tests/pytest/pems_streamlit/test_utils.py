from pathlib import Path

import pytest
from streamlit.navigation.page import StreamlitPage

from pems_streamlit import utils


@pytest.fixture
def test_apps_path():
    return Path(__file__).parent / "test_apps"


@pytest.fixture(autouse=True)
def use_test_apps(mocker, test_apps_path):
    mocker.patch.object(utils, "APP_DIR", test_apps_path)


@pytest.fixture
def app_paths(test_apps_path):
    return [
        test_apps_path / "app_one.py",
        test_apps_path / "app_two.py",
    ]


def test_convert_to_pages(mocker, app_paths):
    page_factory = mocker.patch("pems_streamlit.utils._make_app_page", return_value="page")

    pages = utils._convert_to_pages(app_paths)

    assert len(pages) == len(app_paths)
    for path in app_paths:
        assert mocker.call(path) in page_factory.mock_calls


def test_default_app_page():
    page = utils._default_app_page()

    assert page._default
    assert page.url_path == ""


def test__discover_apps(app_paths):
    discovered = utils._discover_apps()

    assert set(discovered) == set(app_paths)


@pytest.mark.parametrize(
    "filename,result",
    [
        ("app_yes.py", True),
        ("app_definitely-ok.py", True),
        ("not_an_app.py", False),
        ("app_nope.csv", False),
    ],
)
def test_is_app_file(filename, result):
    assert utils._is_app_file(filename) == result


def test_make_app_page(app_paths):
    for path in app_paths:
        page = utils._make_app_page(path)
        assert not page._default


def test_discover_apps(mocker):
    mock_discover = mocker.patch("pems_streamlit.utils._discover_apps", return_value=[])
    mock_convert = mocker.patch("pems_streamlit.utils._convert_to_pages", return_value=[])

    result = utils.discover_apps()

    mock_discover.assert_called_once()
    mock_convert.assert_called_once()

    assert len(result) == 1
    page = result[0]
    assert isinstance(page, StreamlitPage)
    assert page._default

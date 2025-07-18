import pytest

from pems_streamlit import main


@pytest.mark.parametrize(
    "nav_option,expected_nav",
    [
        (None, "hidden"),
        ("hidden", "hidden"),
        ("sidebar", "sidebar"),
        ("invalid", "hidden"),
    ],
)
def test_main(mocker, monkeypatch, nav_option, expected_nav):
    nav_key = "STREAMLIT_NAV"
    apps = ["app", "app"]
    if nav_option:
        monkeypatch.setenv(nav_key, nav_option)
    else:
        monkeypatch.delenv(nav_key, False)

    mock_discover = mocker.patch("pems_streamlit.main.discover_apps", return_value=apps)
    mock_navigate = mocker.patch("pems_streamlit.main.st.navigation")

    main.main()

    mock_discover.assert_called_once()
    mock_navigate.assert_called_once_with(apps, position=expected_nav)
    mock_navigate.return_value.run.assert_called_once()

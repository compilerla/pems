import pytest

from pems_web.core.context_processors import streamlit


@pytest.mark.parametrize("url", ["http://sthost.gov", "http://localhost:8501"])
def test_streamlit(app_request, settings, url):
    """Test that the streamlit context processor returns the correct url."""
    settings.STREAMLIT_URL = url
    context = streamlit(app_request)

    assert context["streamlit"]["url"] == url

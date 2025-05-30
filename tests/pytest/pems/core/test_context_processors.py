import pytest
from pems.core.context_processors import streamlit_host


@pytest.mark.parametrize("host_name", ["localhost", "other.host"])
def test_streamlit_host(app_request, settings, host_name):
    """Test that the streamlit_host context processor returns the correct host."""
    settings.STREAMLIT_HOST = host_name
    context = streamlit_host(app_request)

    assert context["streamlit_host"] == host_name

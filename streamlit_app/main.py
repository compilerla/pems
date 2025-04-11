import logging
import os

import django

import streamlit as st

from streamlit_app.utils import discover_apps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def django_setup():
    """
    Configures Django in case it is not running in the same environment. Should be called before using e.g. PeMS models.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pems.settings")

    django.setup()


def main():
    logger.info("Streamlit initializing")

    django_setup()

    # find apps in the ./streamlit_app/apps directory and subdirectories
    # apps are python modules with a name starting with "app_"
    apps = discover_apps()
    # position=hidden hides the sidebar navigator
    # we just want the multi-page app functionality without the chrome
    # https://docs.streamlit.io/develop/api-reference/navigation/st.navigation#stnavigation
    nav_position = os.environ.get("STREAMLIT_NAV", "hidden")
    site = st.navigation(apps, position=nav_position)

    logger.info("Initialization complete")
    logger.info("Starting streamlit app")

    site.run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

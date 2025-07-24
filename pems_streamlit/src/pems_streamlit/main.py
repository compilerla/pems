import logging
import os

import streamlit as st

from pems_streamlit.utils import discover_apps

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Streamlit initializing")

    # find apps in the ./streamlit_app/apps directory and subdirectories
    # apps are python modules with a name starting with "app_"
    apps = discover_apps()
    # position=hidden hides the sidebar navigator
    # https://docs.streamlit.io/develop/api-reference/navigation/st.navigation#stnavigation
    nav_position = os.environ.get("STREAMLIT_NAV", "hidden")
    if nav_position not in ("hidden", "sidebar"):
        nav_position = "hidden"
    site = st.navigation(apps, position=nav_position)

    logger.info("Initialization complete")
    logger.info("Starting multipage streamlit app")

    site.run()


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

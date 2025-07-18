import logging
from pathlib import Path

import streamlit as st
from streamlit.navigation.page import StreamlitPage

logger = logging.getLogger(__name__)


APP_DIR = Path(__file__).parent / "apps/"


def _convert_to_pages(apps: list[Path]) -> list[StreamlitPage]:
    return list(map(_make_app_page, apps))


def _default_app_page() -> StreamlitPage:
    return st.Page(APP_DIR / "__init__.py", default=True, title="PeMS Streamlit apps")


def _discover_apps() -> list[Path]:
    logger.info("Beginning streamlit app discovery")

    apps = []

    for dirpath, _, filenames in APP_DIR.walk(top_down=True):
        for app_file in filter(_is_app_file, filenames):
            logger.info(f"Discovered streamlit app: {dirpath}/{app_file}")
            apps.append(dirpath / app_file)

    logger.info(f"Discovered {len(apps)} streamlit apps")
    return apps


def _is_app_file(filename: str) -> bool:
    return filename.startswith("app_") and filename.endswith(".py")


def _make_app_page(app_path: Path) -> StreamlitPage:
    relative_dir = app_path.parent.relative_to(APP_DIR)
    app_name = app_path.name.replace("app_", "").replace(".py", "")

    parts = (*relative_dir.parts, app_name)
    url = "--".join(parts)

    title = url.replace("--", " | ").capitalize()

    logger.info(f"Registering streamlit app: {url}")

    return st.Page(app_path, url_path=url, title=title)


def discover_apps() -> list[StreamlitPage]:
    default_app_page = _default_app_page()
    apps = _discover_apps()
    pages = _convert_to_pages(apps)
    pages.insert(0, default_app_page)
    return pages

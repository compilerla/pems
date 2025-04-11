import logging

import streamlit as st

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.info("Starting streamlit")
    st.write("https://pems.dot.ca.gov")


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

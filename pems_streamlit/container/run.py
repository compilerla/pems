#!/usr/bin/env python
import runpy

# since we're installing pems_streamlit as a package now, the main.py file won't exist
# in the running container, so we can't point `streamlit run` at it

# instead, use runpy to run the pems_streamlit.main module directly.

if __name__ == "__main__":
    runpy.run_module("pems_streamlit.main", run_name="__main__", alter_sys=True)

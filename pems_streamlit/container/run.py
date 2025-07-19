#!/usr/bin/env python
import runpy

if __name__ == "__main__":
    runpy.run_module("pems_streamlit.main", run_name="__main__", alter_sys=True)

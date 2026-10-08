"""Kept for old commands: same as build.py."""
import runpy, sys, os
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "build.py"), run_name="__main__")

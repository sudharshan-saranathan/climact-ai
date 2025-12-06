# Encoding: utf-8
# Module name: path
# Description: Path utilities for resource management in Climact-ai application.
# File: `src/climact_ai/path.py`

# Import - standard libraries:
import os
import sys
from typing import AnyStr

if getattr(sys, "frozen", False):
    # If the application is frozen (e.g., packaged with PyInstaller)
    BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    # If the application is running in a normal Python environment
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Function get resource path
def rpath(*parts) -> AnyStr:
    """
    Returns the absolute path to a bundled resource, handling both frozen and non-frozen states.
    :param parts:
    :return str: Absolute path to the resource.
    """
    return os.path.join(BASE_DIR, *parts)


__all__ = ["BASE_DIR", "rpath"]

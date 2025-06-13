"""
This file is used to create the package we'll publish to PyPI.

.. currentmodule:: setup.py
.. moduleauthor:: Mark Steadman <mark@soundslocal.co.uk>
"""

import importlib.util
import os
from pathlib import Path
from setuptools import setup, find_packages
from codecs import open  # Use a consistent encoding.
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# Get the base version from the library. (We'll find it in the `version.py`
# file in the src directory, but we'll bypass actually loading up the library.)
vspec = importlib.util.spec_from_file_location(
  "version",
  str(Path(__file__).resolve().parent /
      "ghostexporter"/"version.py")
)
vmod = importlib.util.module_from_spec(vspec)
vspec.loader.exec_module(vmod)
version = getattr(vmod, "__version__")

# If the environment has a build number set...
if os.getenv("buildnum") is not None:
    # append it to the version.
    version = f"{version}.{os.getenv('buildnum')}"

setup(
    name="podcast-ghost-exporter",
    description="A command-line utility for creating Ghost-compatible JSON documents for importing podcast content.",
    long_description=long_description,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version=version,
    install_requires=[
        "beautifulsoup4>=4,<5",
        "bleach>=6,<7",
        "click>=7.0,<8",
        "feedparser>=6,<7",
        "python-dateutil>=2,<3",
        "python-slugify>=8,<9",
        "PyTZ",
        "requests>=2,<3"
    ],
    entry_points="""
    [console_scripts]
    ghostexporter=ghostexporter.cli:cli
    """,
    python_requires=">=0.0.1",
    license="MIT",
    author="Mark Steadman",
    author_email="mark@soundslocal.co.uk",
    url="https://github.com/hellosteadman/ghostexporter",
    download_url="https://github.com/hellosteadman/ghostexporter/archive/%s.tar.gz" % version,
    keywords=[
        "ghost",
        "podcast",
        "rss"
    ],
    # See https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        """License :: OSI Approved :: MIT License""",
        "Programming Language :: Python :: 3.7"
    ],
    include_package_data=True
)

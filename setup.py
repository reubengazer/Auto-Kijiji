#! /usr/bin/env python3
from setuptools import setup
import sys

# TODO: finish

if sys.version_info[0] < 3: raise Exception("Sorry, you must use Python 3")

# Helper method that will parse __init__.py to extract VERSION
def parse_setup(key):
    part={}
    for line in INIT.splitlines():
        if key in line:
            exec(line, part)
            break
    return(part[key])

# Read and store init file
INIT = open("./auto_kijiji/__init__.py",'r').read()
# The text of the README file
README = open("./README.md",'r').read()

setup(
    name                =   'Auto-Kijiji',
    description         =   "Automatically post and re-post Kijiji top keep ads at the top of the list for free.",
    url                 =   'https://github.com/reubengazer/Auto-Kijiji',
    install_requires    =   ['selenium','pathlib','python-dotenv', 'numpy'],
    version             =   parse_setup('VERSION'),
    packages            =   ['auto_kijiji'],
    entry_points        =   {'console_scripts': ['autokijiji = auto_kijiji.launcher:main'],},
    classifiers         =   ["Programming Language :: Python :: 3"],
    license             =   'MIT',
    long_description    =   README,
    long_description_content_type   =   "text/markdown"
)
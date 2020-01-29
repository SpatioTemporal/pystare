#!/usr/bin/env/python
"""Installation script
"""

import os
from setuptools import setup, Extension


LONG_DESCRIPTION = """ """

if os.environ.get("READTHEDOCS", False) == "True":
    INSTALL_REQUIRES = []
else:
    INSTALL_REQUIRES = ['numpy>=1.16.2', 'shapely>=1.6', 'geopandas>=0.5']

# get all data dirs in the datasets module
data_files = []

setup(
    name="pystare",
    version='0.1',
    description="",
    long_description=LONG_DESCRIPTION,    
    packages = [],
    ext_modules=[Extension(name='_pystare', 
                           sources=['PySTARE.i', 'PySTARE.cpp'], 
                           swig_opts=['-modern', '-c++'],
                           extra_compile_args=['-std=c++11'],
                           libraries=['STARE'],
                           library_dirs=[],       # Location of libSTARE.a
                           include_dirs=[],       # Location of STARE.h
                           language='c++', 
                           )],
    
    python_requires=">=3.5",
    install_requires=INSTALL_REQUIRES,
) 




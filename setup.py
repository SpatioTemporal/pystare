#!/usr/bin/env/python
"""Installation script
"""

import os
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py


LONG_DESCRIPTION = """ """

if os.environ.get("READTHEDOCS", False) == "True":
    INSTALL_REQUIRES = []
else:
    INSTALL_REQUIRES = ['numpy>=1.16.2', 'shapely>=1.6', 'geopandas>=0.5']


class build_py(_build_py):   
    def run(self):
        self.run_command("build_ext")
        return super().run()
    

pystare = Extension(name='_pystare', 
                    sources=['PySTARE.i', 'PySTARE.cpp'], 
                    depends=['PySTARE.h'],
                    swig_opts=['-modern', '-c++'],
                    extra_compile_args=['-std=c++11'],
                    libraries=['STARE'],
                    library_dirs=[],       # Location of libSTARE.a
                    include_dirs=[],       # Location of STARE.h
                    language='c++')


# get all data dirs in the datasets module
data_files = []

setup(
    name='pystare',
    version='0.1',
    description="",
    cmdclass={'build_py': build_py},
    long_description=LONG_DESCRIPTION,         
    py_modules = ['pystare'],
    ext_modules=[pystare],    
    python_requires=">=3.5",
    test_suite='tests',
    install_requires=INSTALL_REQUIRES
) 




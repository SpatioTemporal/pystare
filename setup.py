#!/usr/bin/env/python
"""Installation script
"""

import os
import numpy
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py
import versioneer

LONG_DESCRIPTION = """ """

if os.environ.get("READTHEDOCS", False) == "True":
    INSTALL_REQUIRES = []
else:
    INSTALL_REQUIRES = ['numpy>=1.20.0']

STARE_LIB_DIRS = [os.environ.get('STARE_LIB_DIR', '/usr/local/lib')]
STARE_INCLUDE_DIRS = [os.environ.get('STARE_INCLUDE_DIR', '/usr/local/include')]


if os.environ.get('PYTHON_INCLUDE_DIRS') is None:
    PYTHON_INCLUDE_DIRS = []
else:
    PYTHON_INCLUDE_DIRS = os.environ.get('PYTHON_INCLUDE_DIRS').split(':')

INCLUDE_DIRS = STARE_INCLUDE_DIRS + PYTHON_INCLUDE_DIRS + [numpy.get_include()]


pystare = Extension(name='pystare._core',
                    sources=['pystare/PySTARE.i', 'pystare/PySTARE.cpp'],
                    depends=['pystare/PySTARE.h'],
                    swig_opts=['-modern', '-c++'],
                    extra_compile_args=['-std=c++11'],
                    libraries=['STARE'],
                    library_dirs=STARE_LIB_DIRS,    # Location of libSTARE.a
                    include_dirs=INCLUDE_DIRS,      # Location of STARE.h
                    language='c++')


class BuildPy(_build_py):

    def run(self):
        # Making sure extension is built before getting copied
        self.run_command("build_ext")
        return super().run()


version = versioneer.get_version()
version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()
cmdclass['build_py'] = BuildPy


tests_require = ['matplotlib']


setup(
    setup_requires=["numpy"],
    install_requires=INSTALL_REQUIRES,

    # This would be used by python setup.py tests
    tests_require=tests_require,
    # This is used by tox
    extras_require={
        "test": [tests_require],
        "docs": ["sphinx", "numpydoc"],
    },
    name='pystare',
    version=version,#'0.8.0',
    description="",
    cmdclass={'build_py': BuildPy},
    long_description=LONG_DESCRIPTION,
    packages=["pystare"],
    include_package_data=False,
    ext_modules=[pystare],    
    python_requires=">=3.5",
) 




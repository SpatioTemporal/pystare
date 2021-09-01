#!/usr/bin/env/python
"""Installation script
"""

import os
import numpy
from setuptools import setup, Extension
from setuptools.command.build_py import build_py
from setuptools.command.build_ext import build_ext
import versioneer


STARE_LIB_DIRS = [os.environ.get('STARE_LIB_DIR', '/usr/local/lib')]
STARE_INCLUDE_DIRS = [os.environ.get('STARE_INCLUDE_DIR', '/usr/local/include')]

INCLUDE_DIRS = STARE_INCLUDE_DIRS + [numpy.get_include()]

pystare = Extension(name='pystare._core',
                    sources=['pystare/PySTARE.i', 'pystare/PySTARE.cpp'],
                    swig_opts=['-c++'],
                    extra_compile_args=['-std=c++11'],
                    libraries=['STARE'],
                    library_dirs=STARE_LIB_DIRS,    # Location of libSTARE.a
                    include_dirs=INCLUDE_DIRS,      # Location of STARE.h
                    language='c++')


class BuildPy(build_py):

    def run(self):
        """ 
        We need to overwrite run to make sure extension is built before getting copied
        """
        self.run_command("build_ext")
        return super().run()

version = versioneer.get_version()

cmdclass = versioneer.get_cmdclass()
cmdclass['build_py'] = BuildPy
cmdclass['build_ext'] = build_ext


setup(
    #version="0.8.2",
    version=version,
    cmdclass=cmdclass,    
    ext_modules=[pystare],
) 




#!/usr/bin/env/python

import os
import numpy
from setuptools import setup, Extension
from setuptools.command.build_py import build_py as _build_py
from setuptools.command.build_ext import build_ext as build_ext
import versioneer

STARE_LIB_DIRS = [os.path.expanduser(os.environ.get('STARE_LIB_DIR', '/usr/local/lib/'))]
STARE_INCLUDE_DIRS = [os.path.expanduser(os.environ.get('STARE_INCLUDE_DIR', '/usr/local/include/STARE/'))]

INCLUDE_DIRS = STARE_INCLUDE_DIRS + [numpy.get_include()] + ['pystare/numpy.i', 'pystare/PySTARE.h']

pystare = Extension(name='pystare._core',
                    sources=['pystare/PySTARE.i', 'pystare/PySTARE.cpp'],
                    swig_opts=['-c++'],
                    extra_compile_args=['-std=c++11'],
                    libraries=['STARE'],
                    library_dirs=STARE_LIB_DIRS,    # Location of libSTARE.a
                    include_dirs=INCLUDE_DIRS,      # Location of STARE.h
                    language='c++')


class build_py(_build_py):

    def run(self):
        """ 
        We need to overwrite run to make sure extension is built before getting copied
        """
        self.run_command("build_ext")
        return super().run()


version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()
#cmdclass['build_py'] = build_py
#cmdclass['build_ext'] = build_ext


setup(
    version=version,
    cmdclass=cmdclass,    
    ext_modules=[pystare],
) 

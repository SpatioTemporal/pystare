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

STARE_LIB_DIRS = [os.environ.get('STARE_LIB_DIR', '/home/jovyan/users_conda_envs/work/lib')]
STARE_INCLUDE_DIRS = [os.environ.get('STARE_INCLUDE_DIR','/home/jovyan/users_conda_envs/work/include')]

PYTHON_INCLUDE_DIRS = [] if os.environ.get('PYTHON_INCLUDE_DIRS') is None else os.environ.get('PYTHON_INCLUDE_DIRS').split(':')

INCLUDE_DIRS = STARE_INCLUDE_DIRS + PYTHON_INCLUDE_DIRS + [numpy.get_include()]

EXTRA_COMPILE_ARGS=['-std=c++11']
LIBRARIES=['STARE']

#########
### Just to get started...
### Check for OpenMP -- cf. https://stackoverflow.com/questions/16549893/programatically-testing-for-openmp-support-from-a-python-setup-script
import os, tempfile, subprocess, shutil

CC              = 'cc'       if os.environ.get('CC') is None else os.environ.get("CC")
OMP_CFLAGS      = '-fopenmp' if os.environ.get('OMP_CFLAGS') is None else os.environ.get("OMP_CFLAGS")
OMP_INCLUDE_DIR = None       if os.environ.get('OMP_INCLUDE_DIR') is None else os.environ.get('OMP_INCLUDE_DIR')
OMP_LIB_DIR     = None       if os.environ.get('OMP_LIB_DIR') is None else os.environ.get('OMP_LIB_DIR')
OMP_LIBRARY     = 'gomp'     if os.environ.get('OMP_LIBRARY') is None else os.environ.get('OMP_LIBRARY')

OMP_LDFLAGS = [] if OMP_LIB_DIR is None else ['-L'+OMP_LIB_DIR]
OMP_LDFLAGS = OMP_LDFLAGS + ['-l'+OMP_LIBRARY]

OMP_CFLAGS = OMP_CFLAGS.split(' ') if OMP_INCLUDE_DIR is None else ['-I'+OMP_INCLUDE_DIR] + OMP_CFLAGS.split(' ')

TEST_FLAGS = OMP_CFLAGS + OMP_LDFLAGS

# see http://openmp.org/wp/openmp-compilers/
omp_test = \
r"""
#include <omp.h>
#include <stdio.h>
int main() {
#pragma omp parallel
printf("Hello from thread %d, nthreads %d\n", omp_get_thread_num(), omp_get_num_threads());
}
"""

def check_for_openmp():
    tmpdir = tempfile.mkdtemp()
    curdir = os.getcwd()
    os.chdir(tmpdir)

    filename = r'test.c'
    with open(filename, 'w') as file:
        file.write(omp_test)
    with open(os.devnull, 'w') as fnull:
        FLAGS= (' '.join(TEST_FLAGS)).split(' ')
        CMD=[CC] + FLAGS + [filename]
        # print('CMD: ',CMD)
        result = subprocess.call(CMD,stdout=fnull,stderr=fnull)
        # print(os.listdir('.'))
        if result == 0:
            result = subprocess.call(['./a.out'],stdout=fnull,stderr=fnull)
    os.chdir(curdir)
    #clean up
    shutil.rmtree(tmpdir)

    return result

if check_for_openmp() == 0:
    print('OpenMP found. Adding build options.')
    EXTRA_COMPILE_ARGS  = EXTRA_COMPILE_ARGS + OMP_CFLAGS + OMP_LDFLAGS
    LIBRARIES           = LIBRARIES + [OMP_LIBRARY]
else:
    print('OpenMP not found. Continuing...')

########

pystare = Extension(name='pystare._core',
                    sources=['pystare/PySTARE.i', 'pystare/PySTARE.cpp'],
                    depends=['pystare/PySTARE.h'],
                    swig_opts=['-modern', '-c++'],
                    extra_compile_args=EXTRA_COMPILE_ARGS,
                    libraries=LIBRARIES,
                    library_dirs=STARE_LIB_DIRS,    # Location of libSTARE.a
                    include_dirs=INCLUDE_DIRS,      # Location of STARE.h
                    language='c++')


class BuildPy(_build_py):

    def run(self):
        # Making sure extension is built before getting copied
        self.run_command("build_ext")
        return super().run()


version = versioneer.get_version()
cmdclass = versioneer.get_cmdclass()
cmdclass['build_py'] = BuildPy

setup(
    setup_requires=["numpy"],
    name='pystare',
    version=version,
    description="",
    cmdclass={'build_py': BuildPy},
    long_description=LONG_DESCRIPTION,
    packages=["pystare"],
    include_package_data=False,
    ext_modules=[pystare],    
    python_requires=">=3.5",
    install_requires=INSTALL_REQUIRES
) 




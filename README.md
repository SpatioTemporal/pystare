# PySTARE

## Introduction
PySTARE exposes the STARE library to python.


## Requirements
Pystare requires STARE to be installed.
It expects either:

- ```libSTARE.a``` in /usr/local/lib/ and STARE.h in /usr/local/include/ or
- the variables STARE_LIB_DIR and STARE_INCLUDE_DIR to be set e.g. with:

```bash
export STARE_INCLUDE_DIR=/path/to/directory-containing-stare.h/
export STARE_LIB_DIR=/path/to/directory-containing-stare.a/
```


Build and install STARE e.g. with:

```bash
git clone https://github.com/SpatioTemporal/STARE
cd STARE
mkdir build
cd build
cmake -DSTARE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=NO ../
make -j4
sudo make install
```


It may be necessary to set PYTHON_INCLUDE_DIRS, if, for example, numpy
headers cannot be found.

## Installation on Linux
Wheels for manylinux exist on pypi
 
```bash
pip install pystare
```

### Install from source:

```bash
export STARE_INCLUDE_DIR=/path/to/directory-containing-stare.h/
export STARE_LIB_DIR=/path/to/directory-containing-stare.a/
        
git clone https://github.com/SpatioTemporal/pystare 
pip3 install pystare/
```
    
### (Optional) Manual build from source

```shell
python3 setup.py build_ext --inplace 
python3 setup.py bdist_wheel
python3 setup.py sdist
```

## Manual Installation on MacOS M1

#### I.Install STARE on MacOS M1
1. Create new conda env with python 3.12:     

`conda create -n <YOUR_CONDA_ENV> python=3.12`

E.g: `conda create -n stare_3.12 python=3.12`

2. Activate conda env:

`conda activate <YOUR_CONDA_ENV>`  

E.g: `conda activate stare_3.12`
3. Install numpy: 

`conda install -c conda-forge numpy`  

4. Install cmake: 

```
sudo apt update  
sudo apt install cmake
```

or: 

`conda install -c conda-forge cmake`

5. Install doxygen & x-code-select:

```
conda install -c conda-forge doxygen
xcode-select --install
```

6. (Optional) May need to link librhash library
```
cd /Users/tonhai/miniconda3/envs/<YOUR_CONDA_ENV>/lib
ln -s librhash.<VERSION>.dylib librhash.0.dylib
```
E.g:
```
cd /Users/tonhai/miniconda3/envs/stare_3.12/lib
ln -s librhash.1.4.5.dylib librhash.0.dylib
```

7. Download & install STARE from source:

```
git clone https://github.com/SpatioTemporal/STARE  
cd STARE
mkdir build
cd build
cmake -DCMAKE_OSX_ARCHITECTURES=arm64 \
      -DCMAKE_OSX_SYSROOT="$(xcode-select --print-path)/SDKs/MacOSX.sdk" \
      -DCMAKE_OSX_DEPLOYMENT_TARGET=11.0 \
      -DCMAKE_CXX_FLAGS="-isysroot $(xcode-select --print-path)/SDKs/MacOSX.sdk -I$(xcode-select --print-path)/SDKs/MacOSX.sdk/usr/include/c++/v1" \
      -DSTARE_INSTALL_LIBDIR=lib \
      -DBUILD_SHARED_LIBS=NO \
      ../
make -j4
sudo make install
```

8. Check to see if libSTARE.a in /usr/local/lib/ and STARE.h in /usr/local/include/, if not: 
```
export STARE_INCLUDE_DIR=/path/to/directory-containing-stare.h/  
export STARE_LIB_DIR=/path/to/directory-containing-stare.a/
```
       
E.g.: 
```
export STARE_INCLUD_DIR=/Users/tonhai/miniconda3/envs/stare_3.12/include/STARE
export STARE_LIB_DIR=/Users/tonhai/miniconda3/envs/stare_3.12/lib
```

```
python3 setup.py build_ext --inplace 
python3 setup.py bdist_wheel
python3 setup.py sdist
```

#### II. Install pystare on MacOS M1
1. Install setuptools, swig and wheel: 

`conda install -c conda-forge setuptools swig wheel`

2. Download pystare, rebuild and install:
```
git clone https://github.com/SpatioTemporal/pystare  
cd pystare  
export CXXFLAGS="-I$(xcode-select --print-path)/SDKs/MacOSX.sdk/usr/include/c++/v1"
python3 setup.py build_ext --inplace  
python3 setup.py bdist_wheel  
python3 setup.py sdist  
pip3 install .  
```

If there is any issue, try to export this and retry:

`export CXXFLAGS="-I/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/usr/include/c++/v1"`

## Tests
pystare uses [pytest](https://docs.pytest.org/en/6.2.x/). Pytest is configured in ```pytest.ini.```

Run ```pytest``` to run all tests.

To run the doctest,

```shell
pytest --doctest-modules 
```

To run tests of a specific module

```shell
pytest /path/to/module.py
```

## Documentation
pystare uses sphinx

```bash
pip install sphinx-markdown-tables 
            sphinx-automodapi 
            myst_parser 
            nbsphinx 
            numpydoc 
            pydata-sphinx-theme
```


## Usage

### Spatial
```python
import numpy
import pystare
    

lat = numpy.array([30,45,60], dtype=numpy.double)
lon = numpy.array([45,60,10], dtype=numpy.double)

indices = pystare.from_latlon(lat, lon, 12)
print('0 indices: ', [hex(i) for i in indices])

lat, lon = pystare.to_latlon(indices)
print(lat, lon)

lat, lon, level = pystare.to_latlonlevel(indices)
print(lat, lon, level)

level = pystare.to_level(indices)
print(level)

area = pystare.to_area(indices)
print(area)
```
 

### Temporal
```python
import numpy
import pystare

datetime = numpy.array(['1970-01-01T00:00:00', 
                        '2000-01-01T00:00:00', 
                        '2002-02-03T13:56:03.172', 
                        '2016-01-05T17:26:00.172'], dtype=numpy.datetime64)
print(datetime)
print(datetime.astype(numpy.int64))
    
index = pystare.from_ms_since_epoch_utc(datetime.astype(numpy.int64), 6, 6)
print([hex(i) for i in index])

index = pystare.from_ms_since_epoch_utc(datetime.astype(numpy.int64), 27, 27)
print([hex(i) for i in index])

```


    
### Common issues when building
`undefined symbol`

1. STARE and pystare out of sync. Are we building against the correct STARE version?
2. Stale pystare targets. `python setup.py clean` might help
3. Missing function headers in `PySTARE.h`

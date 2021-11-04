# PySTARE

## Introduction
PySTARE exposes the STARE library to python.


## Requirements
Pystare requires STARE to be installed.
It expects either:

- ```libSTARE.a``` in /usr/local/lib/ and STARE.h in /usr/local/include/ or
- the variables STARE_LIB_DIR and STARE_INCLUDE_DIR to be set e.g. with:

```shell
export STARE_INCLUDE_DIR=/path/to/directory-containing-stare.h/
export STARE_LIB_DIR=/path/to/directory-containing-stare.a/
```


Build and install STARE e.g. with:

    git clone https://github.com/SpatioTemporal/STARE
    cd STARE
    mkdir build
    cd build
    cmake -DSTARE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=NO ../
    make -j4
    sudo make install


It may be necessary to set PYTHON_INCLUDE_DIRS, if, for example, numpy
headers cannot be found.

## Installation
Wheels for manylinux exist on pypi
 
    pip install pystare==0.8.1

### Or install from source:

    export STARE_INCLUDE_DIR=/path/to/directory-containing-stare.h/
    export STARE_LIB_DIR=/path/to/directory-containing-stare.a/
        
    git clone https://github.com/SpatioTemporal/pystare 
    pip3 install pystare/
    
### Manual build

```shell
python3 setup.py build_ext --inplace 
python3 setup.py bdist_wheel
python3 setup.py sdist
```
    
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

```shell
pip install sphinx-markdown-tables sphinx-automodapi myst_parser nbsphinx numpydoc pydata-sphinx-theme
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
    
index = pystare.from_utc(datetime.astype(numpy.int64), 6)
print([hex(i) for i in index])

index = pystare.from_utc(datetime.astype(numpy.int64), 27)
print([hex(i) for i in index])

```


    




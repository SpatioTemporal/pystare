git clone https://github.com/SpatioTemporal/STARE
cd STARE
set -x # Print commands and their arguments as they are executed.
mkdir build
cd build
#cmake -DCMAKE_INSTALL_PREFIX=~/stare ..
cmake ../
make
make install

# Set environment vars for setup.py
#STARE_LIB_DIR=~/stare/lib/
#STARE_INCLUDE_DIR=~/stare/include/
#CPPFLAGS: "-I/usr/include -I/usr/local/include -I/home/runner/stare/include"
#LDFLAGS: "-L/home/runner/stare/lib"

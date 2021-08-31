git clone https://github.com/SpatioTemporal/STARE
cd STARE
set -x
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX=~/stare ..
make
make install
STARE_LIB_DIR=~/stare/lib/
STARE_INCLUDE_DIR=~/stare/include/
CPPFLAGS: "-I/usr/include -I/usr/local/include -I/home/runner/stare/include"
LDFLAGS: "-L/home/runner/stare/lib"

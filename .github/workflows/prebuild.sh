# This script clones, builds and installs STARE

git clone https://github.com/SpatioTemporal/STARE
cd STARE

# Print commands and their arguments as they are executed.
set -x 

mkdir build
cd build

# We install STARE to /usr/local/include/STARE/ and /usr/local/lib/ .. seems easist.
cmake -DSTARE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=NO ..
make -j4
make install

# This script clones, builds and installs STARE

git clone https://github.com/SpatioTemporal/STARE
cd STARE

# Print commands and their arguments as they are executed.
set -x 

mkdir build
cd build

# We install STARE to /usr/local/include/ and /usr/local/lib/ .. seems easist.
cmake ../ 
make
make install

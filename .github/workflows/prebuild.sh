# This script clones, builds and installs STARE

git clone https://github.com/SpatioTemporal/STARE
cd STARE

# Print commands and their arguments as they are executed.
set -x 

mkdir build
cd build

# We install STARE to /usr/local/include/STARE/ and /usr/local/lib/ .. seems easist.
#cmake -DSTARE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=NO ..
cmake -DCMAKE_INSTALL_PREFIX=~/stare -DSTARE_INSTALL_LIBDIR=lib -DBUILD_SHARED_LIBS=NO ..
make -j4
make install

cd

# To fix git security enhancement, we need to add pystare as a safe directory
# https://github.blog/2022-04-12-git-security-vulnerability-announced/
# https://github.com/multi-build/multibuild/issues/470
git config --global --add safe.directory "*"

export STARE_LIB_DIR=~/stare/lib/
export STARE_INCLUDE_DIR=~/stare/include/STARE/
        
        
        

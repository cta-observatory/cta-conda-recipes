mkdir build
cd build
CC=gcc-8 CXX=g++-8 cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$PREFIX
make
make install

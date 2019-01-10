mkdir build
cd build
CC=gcc CXX=g++ cmake .. -DCMAKE_INSTALL_PREFIX:PATH=$PREFIX
make
make install

#!/bin/bash
# Onetime slideToolkit install script for Ubuntu
# Do not use this script, it is build for testing purposes.
# B. Nelissen

# Check Ubuntu version
if [[ "12.04" != "$(lsb_release -r | awk '{print $2}')" ]]; then
  echo "No Ubuntu 12.04 LTS found."
  exit 1
fi

# Let's roll
# step 1
sudo apt-get --yes update && \
sudo apt-get --yes upgrade && \
sudo apt-get --yes dist-upgrade && \
sudo apt-get --yes autoremove
if [[ $? != 0 ]]; then echo "Error in step 1"; exit 1; fi

# step 2
sudo apt-get --yes update && \
sudo apt-get --yes install autoconf automake "build-essential" cvs gimp git "libgtk2.0-dev" "libjpeg-dev" "libopenjpeg-dev" "libopenslide-dev" "libsqlite3-dev" libtool "libxml2-dev" parallel perl "pkg-config" vim wget wmctrl "zbar-tools"
if [[ $? != 0 ]]; then echo "Error in step 2"; exit 1; fi

# step 3
mkdir -p ~/src && cd ~/src && \
wget http://zlib.net/zlib-1.2.8.tar.gz -O zlib-1.2.8.tar.gz && \
tar xzvf zlib-1.2.8.tar.gz && \
rm zlib-1.2.8.tar.gz
cd ~/src/zlib-1.2.8 && \
./configure && \
make && \
sudo make install && \
make clean
if [[ $? != 0 ]]; then echo "Error in step 3"; exit 1; fi

# step 4
mkdir -p ~/cvs && \
cd ~/cvs && \
cvs -d :pserver:cvsanon:@cvs.maptools.org:/cvs/maptools/cvsroot checkout libtiff && \
cd ~/cvs/libtiff && \
./configure && \
make && \
sudo make install && \
make clean
if [[ $? != 0 ]]; then echo "Error in step 4"; exit 1; fi

# step 5
mkdir -p ~/src/ && cd ~/src
wget http://www.imagemagick.org/download/ImageMagick.tar.gz -O ImageMagick.tar.gz && \
    tar xzfv ImageMagick.tar.gz && \
    rm ImageMagick.tar.gz
cd ~/src/ImageMagick*
./configure && make && sudo make install && make clean
sudo ldconfig /usr/local/lib
if [[ $? != 0 ]]; then echo "Error in step 5"; exit 1; fi

# step 6
mkdir -p ~/git/ && cd ~/git && \
if [ -d ~/git/openslide/.git ]; then \
        cd ~/git/openslide && \
        git pull; \
    else \
        cd ~/git/ && \
        git clone git://github.com/openslide/openslide.git && \
fi && \
cd ~/git/openslide && \
autoreconf -i && \
./configure && \
make && \
sudo make install && \
make clean
if [[ $? != 0 ]]; then echo "Error in step 6"; exit 1; fi

# step 7
mkdir -p ~/usr && \
cd ~/usr && \
wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
unzip -o bftools.zip && \
rm bftools.zip && \
printf "\n# Add the bfconvert directory to the PATH \nPATH=\"$HOME/usr/bfconvert:\$PATH\" \n\n" >> ~/.profile
if [[ $? != 0 ]]; then echo "Error in step 7"; exit 1; fi

# step 8
mkdir -p ~/git/ && \
cd ~/git
if [ -d ~/git/libdmtx/.git ]; then \
        cd ~/git/libdmtx && \
        git pull; \
    else \
        cd ~/git/ && \
        git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/libdmtx; \
    fi && \
cd ~/git/libdmtx && \
mkdir -p m4 && \
autoreconf --force --install && \
./configure && \
make && \
sudo make install && \
make clean && \
mkdir -p ~/git/ && \
cd ~/git && \
if [ -d ~/git/dmtx-utils/.git ]; then \
        cd ~/git/dmtx-utils && \
        git pull; \
    else \
        cd ~/git/ && \
        git clone git://git.code.sf.net/p/libdmtx/dmtx-utils; \
    fi &&\
 cd ~/git/dmtx-utils && \
mkdir -p m4 && \
autoreconf --force --install && \
./configure && \
make && \
sudo make install && \
make clean
if [[ $? != 0 ]]; then echo "Error in step 8"; exit 1; fi

# step 9
mkdir -p ~/git/ && \
cd ~/git && \
if [ -d ~/git/slideToolkit/.git ]; then \
        cd ~/git/slideToolkit && \
        git pull; \
    else \
        cd ~/git/ && \
        git clone https://github.com/bglnelissen/slideToolkit.git; \
    fi && \
printf "\n# Add the slideToolkit directory to the PATH \nPATH=\"$HOME/git/slideToolkit:\$PATH\" \n\n" >> ~/.profile
if [[ $? != 0 ]]; then echo "Error in step 9"; exit 1; fi

# step 10
sudo ldconfig && \
sudo reboot
if [[ $? != 0 ]]; then echo "Error in step 10"; exit 1; fi


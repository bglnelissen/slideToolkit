#!/bin/bash
# slideToolkit installer 16.04
# B. Nelissen

# A set of oneliners for different dependencies for the slideToolkit
# Run these commands in the following order.
# The script will pause on errors or sudo password input.

# add ~/bin to the local enviroment within ~/.profile
if ! [[ "$PATH" =~ (:$HOME/bin:|:~/bin:) ]] ; then mkdir -p ~/bin && printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.profile; fi; PATH="~/bin:$PATH"; export PATH

# update
MESSAGE="slideToolkit installer: apt-get update & upgrade"
if sudo apt-get --yes update && sudo apt-get --yes upgrade && sudo apt-get --yes dist-upgrade && sudo apt-get --yes autoremove; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi

# libraries and packages using apt-get
MESSAGE="slideToolkit installer: install libraries and packages using apt-get"
if sudo apt-get --yes update && sudo apt-get --yes install autoconf automake "build-essential" curl cvs gimp git "libdmtx-utils" "libgtk2.0-dev" "libjpeg-dev" "libopenjpeg-dev" "libopenslide-dev" "libpng-dev" "libsqlite3-dev" libtool "libxml2-dev" parallel perl "pkg-config" vim wget wmctrl "zbar-tools" zlib1g-dev; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi

# libtiff
MESSAGE="slideToolkit installer: install libtiff"
if mkdir -p ~/cvs && cd ~/cvs && cvs -d :pserver:cvsanon:@cvs.maptools.org:/cvs/maptools/cvsroot checkout libtiff && cd ~/cvs/libtiff && ./configure && make && sudo make install && make clean; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi

# ImageMagick
MESSAGE="slideToolkit installer: install ImageMagick"
if mkdir -p ~/src/ && cd ~/src && wget http://www.imagemagick.org/download/ImageMagick.tar.gz -O ImageMagick.tar.gz && tar xzfv ImageMagick.tar.gz && rm ImageMagick.tar.gz && cd ~/src/ImageMagick* && ./configure && make && sudo make install && make clean && sudo ldconfig /usr/local/lib; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi

# openslide
MESSAGE="slideToolkit installer: install openslide"
if mkdir -p ~/git/ && cd ~/git && if [ -d ~/git/openslide/.git ]; then cd ~/git/openslide && git pull; else cd ~/git/ && git clone git://github.com/openslide/openslide.git; fi && cd ~/git/openslide && autoreconf -i && ./configure && make && sudo make install && make clean; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi

# bfconfert (add the bfconvert dir to the path)
MESSAGE="slideToolkit installer: install bftools"
if mkdir -p ~/usr && cd ~/usr && wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip  -O bftools.zip && unzip -o bftools.zip && rm bftools.zip && mkdir -p ~/bin && ln -sfv ~/usr/bfconvert ~/usr/domainlist ~/usr/formatlist ~/usr/ijview ~/usr/mkfake ~/usr/showinf ~/usr/tiffcomment ~/usr/xmlindent ~/usr/xmlvalid ~/bin/ ; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi

# slideToolkit
MESSAGE="slideToolkit installer: slideToolkit scripts"
if mkdir -p ~/git/ && cd ~/git && if [ -d ~/git/slideToolkit/.git ]; then cd ~/git/slideToolkit && git pull; else cd ~/git/ && git clone https://github.com/bglnelissen/slideToolkit.git; fi && mkdir -p ~/bin/ && ln -s -f -v ~/git/slideToolkit/slide* ~/bin/
RESULT=$?; PACKAGENAME="slideToolkit" if [ $RESULT -eq 0 ]; then echo "$MESSAGE" "(Succes)"; sleep 2; else read -n1 -rsp "$MESSAGE (Fail)" && echo; fi
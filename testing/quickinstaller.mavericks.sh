#!/bin/bash
# Onetime slideToolkit install script for Ubuntu
# Do not use this script, it is build for testing purposes.
# B. Nelissen

# Check Ubuntu version
if ! [[ "$(sw_vers -productVersion)" =~ (^10.9) ]]; then
  echo "No OS X 10.9 Mavericks found."
  exit 1
fi

# Let's roll
echo "Starting with step 1"
if ! [[ "$PATH" =~ (:$HOME/bin:|:~/bin:) ]] ; then \
    mkdir -p ~/bin && \
    printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.bash_profile
    fi
if [[ $? != 0 ]]; then echo "Error in step 1. Exit."; exit 1;else echo "Succes - step 1"; fi

echo "Starting with step 2"
open -R -a XQuartx
if [[ $? != 0 ]]; then
    echo "XQuartz not found. You need to install XQuartz yourself"
    echo "Go go http://xquartz.macosforge.org"
    read -p "Press [Enter] if you did install XQuartz"
fi
if [[ $? != 0 ]]; then echo "Error in step 2. Exit."; exit 1;else echo "Succes - step 2"; fi

echo "Starting with step 3"
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)" && \
brew doctor && \
brew update && brew upgrade
if [[ $? != 0 ]]; then echo "Error in step 3. Exit."; exit 1;else echo "Succes - step 3"; fi

echo "Starting with step 4"
brew install automake wget jpeg libpng libtiff parallel openslide wmctrl zbar && \
brew uninstall --force imagemagick && \
    brew install imagemagick --with-libpng --with-libtiff --with-x11 --build-from-source
if [[ $? != 0 ]]; then echo "Error in step 4. Exit."; exit 1;else echo "Succes - step 4"; fi

echo "Starting with step 5"
parallel --bibtex
if [[ $? != 0 ]]; then echo "Error in step 5. Exit."; exit 1;else echo "Succes - step 5"; fi

echo "Starting with step 6"
mkdir -p ~/usr && cd ~/usr && \
wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
    unzip -o bftools.zip && \
    rm bftools.zip && \
    mkdir -p ~/bin/ && ln -s -f -v ~/usr/bftools/bfconvert ~/bin/ && \
    ln -s -f -v ~/usr/bftools/domainlist ~/bin/ && \
    ln -s -f -v ~/usr/bftools/formatlist ~/bin/ && \
    ln -s -f -v ~/usr/bftools/ijview ~/bin/ && \
    ln -s -f -v ~/usr/bftools/mkfake ~/bin/ && \
    ln -s -f -v ~/usr/bftools/showinf ~/bin/ && \
    ln -s -f -v ~/usr/bftools/tiffcomment ~/bin/ && \
    ln -s -f -v ~/usr/bftools/xmlindent ~/bin/ && \
    ln -s -f -v ~/usr/bftools/xmlvalid ~/bin/
if [[ $? != 0 ]]; then echo "Error in step 6. Exit."; exit 1;else echo "Succes - step 6"; fi

echo "Starting with step 7"
mkdir -p ~/git/ && cd ~/git && \
if [ -d ~/git/libdmtx/.git ]; then \
        cd ~/git/libdmtx && git pull; \
    else \
        cd ~/git/ && git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/libdmtx; \
    fi
cd ~/git/libdmtx && ./autogen.sh && ./configure && make && make install && \
mkdir -p ~/git/ && cd ~/git && \
if [ -d ~/git/dmtx-utils/.git ]; then \
        cd ~/git/dmtx-utils && git pull; \
    else \
        cd ~/git/ && git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/dmtx-utils; \
    fi
cd ~/git/dmtx-utils && ./autogen.sh && ./configure && make && make install
if [[ $? != 0 ]]; then echo "Error in step 7. Exit."; exit 1;else echo "Succes - step 7"; fi

echo "Starting with step 8"
mkdir -p ~/git/ && cd ~/git && \
if [ -d ~/git/slideToolkit/.git ]; then \
        cd ~/git/slideToolkit && git pull; \
    else \
        cd ~/git/ && git clone https://github.com/bglnelissen/slideToolkit.git; \
    fi
mkdir -p ~/bin/ && ln -s -f -v ~/git/slideToolkit/slide* ~/bin/
if [[ $? != 0 ]]; then echo "Error in step 8. Exit."; exit 1;else echo "Succes - step 8"; fi

echo "Starting with step 9"
echo "All done. Restart in 10 seconds" && sleep 10 && sudo reboot
if [[ $? != 0 ]]; then echo "Error in step 9. Exit."; exit 1;else echo "Succes - step 9"; fi

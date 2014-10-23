OS X 10.9 Mavericks - slideToolkit installation instructions
============

The slideToolkit is a set of scripts that requires other programs and libraries to run. Here we explain the dependencies and show instructions on how to install these dependencies. The required dependencies can change and might break your curren slideToolkit installation. Please tell us if you run into problems, it is likely we can help you out.

I tried to create as few steps as possible with one-liners that are *easy* to read. Most of the installation is done using the commandline. You can copy/paste each example command, per block of code. For some steps you need administrator privileges. Follow the steps in consecutive order.

```
these `mono-type font` illustrate commands illustrate terminal commands. You can copy & paste these.
```

To make it easier to copy and paste, long commands that stretch over multiple lines are structed as follows:

```
Multiline commands end with a dash \
	indent 4 spaces, and continue on the next line. \
	Copy & paste these whole blocks of code.
```

--------------

#### Step 1 - Preparations
The system must be up-to-date. Go to the Apple menu on the top left, click "Software Update...", and click the "Update all" button. Make shure you stay on 'OS X 10.9 Mavericks'. If the system asks you if you want to turn on automatic updates, select 'Turn on'. Restart your system if needed.

Binairies are executed from your local `bin` folder. By default this folder does not exists and is not present in your PATH. Create your `~/bin` and add it to your PATH if needed.

```
if ! [[ "$PATH" =~ (:$HOME/bin:|:~/bin:) ]] ; then \
	mkdir -p ~/bin && \
	printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.bash_profile
	fi
```

#### Step 2 - Install XQuartz, a version of the X.Org X Window System that runs on OS X
XQuartz is needed. Go to [xquartz.macosforge.org](http://xquartz.macosforge.org), download and install the latest stable version of XQuartz (about 70mb). You can find it under "Quick Download".

On the end of the installation you are asked to log out and log back in, and of course you comply.

#### Step 3 - Install brew 🍺, the missing package manager for OS X
We install [brew](http://brew.sh) using the following one-liner. You need administrator rights for the installation. No characters will appear on the screen when you type in your password. Paste the following oneliner in your the terminal.

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

When asked if you want to install the "command line developer tools", choose 'Install'. After the "command line developer tools" installation, continue the installation in the Terminal

After a `brew` installation, it is wise to do a `brew doctor` and follow the instructions on the screen.

```
brew doctor
```
A final update and upgrade for your `brew` packages

```
brew update && brew upgrade
```

From now on, we asume your `brew` package manager is good to go.

#### Step 4 - Install packages using brew
We install most packages using brew.

```
brew install automake wget jpeg libpng libtiff parallel openslide wmctrl zbar
```
Uninstall previous installations of imagemagick first before we build it from source, and it with the extra libraries.

```
brew uninstall --force imagemagick && \
    brew install imagemagick --with-libpng --with-libtiff --with-x11 --build-from-source
```

#### Step 5 - Install the bioformat tools
Install the latest version of BioFormats, including `bfconvert`.

```
mkdir -p ~/usr && cd ~/usr
```
```
wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
	unzip -o bftools.zip && \
	rm bftools.zip
```
Add symbolic links in `~/bin/`. Now the BioFormats tools will be availabe in your PATH. Adding the bftools  to your PATH is obligatory for the slideToolkit to find its dependencies.

```
mkdir -p ~/bin/ && ln -s -f -v ~/usr/bftools/bfconvert ~/bin/ && \
    ln -s -f -v ~/usr/bftools/domainlist ~/bin/ && \
    ln -s -f -v ~/usr/bftools/formatlist ~/bin/ && \
    ln -s -f -v ~/usr/bftools/ijview ~/bin/ && \
    ln -s -f -v ~/usr/bftools/mkfake ~/bin/ && \
    ln -s -f -v ~/usr/bftools/showinf ~/bin/ && \
    ln -s -f -v ~/usr/bftools/tiffcomment ~/bin/ && \
    ln -s -f -v ~/usr/bftools/xmlindent ~/bin/ && \
    ln -s -f -v ~/usr/bftools/xmlvalid ~/bin/
```

#### Step 6 - Install datamatrix barcode libraries
Install the latest version of libdmtx, including `dmtxread`. First we install the libraries:

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/libdmtx/.git ]; then \
		cd ~/git/libdmtx && git pull; \
	else \
		cd ~/git/ && git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/libdmtx; \
	fi
```
```
cd ~/git/libdmtx && ./autogen.sh && ./configure && make && make install
```

Now we install the binairies:

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/dmtx-utils/.git ]; then \
		cd ~/git/dmtx-utils && git pull; \
	else \
		cd ~/git/ && git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/dmtx-utils; \
	fi
```
```
cd ~/git/dmtx-utils && ./autogen.sh && ./configure && make && make install
```
The dmtx binairies are installed in `/usr/local/bin`. This is the same folder `brew` uses for its installations and should already be in your PATH.

#### Step 7 - Download the slideToolkit
Download and setup the latest version of the slideToolkit.

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/slideToolkit/.git ]; then \
		cd ~/git/slideToolkit && git pull; \
	else \
		cd ~/git/ && git clone https://github.com/bglnelissen/slideToolkit.git; \
	fi
```

Add symbolic links in `~/bin/`. Now the slideToolkit will be availabe in your PATH. Adding the slideToolkit tools to your PATH makes it easier to acces the slideToolkit commands.

```
mkdir -p ~/bin/ && ln -s -f -v ~/git/slideToolkit/slide* ~/bin/
```

#### Step 8 - CellProfiler
Install CellProfiler following instructions on their [website](http://cellprofiler.org/download.shtml). Install CellProfiler on the default location.

Now create a link in your `~/bin` to make cellprofiler accessible for the commandline.

```
printf '#!/bin/bash\n# run cellprofiler from CLI\n/Applications/CellProfiler.app/Contents/MacOS/CellProfiler "$@"\n' \
    > ~/bin/cellprofiler && chmod 755 ~/bin/cellprofiler

```

#### Step 9 - Reboot
Restart and you're done.

---

<a name="ubuntu_12.04"></a>
Ubuntu 12.04 - slideToolkit installation instructions
--------------

#### Step 1 - Make shure you have the 'latest & greatest'
The system must be up-to-date. Install updates, answer --yes to everything. Make sure you stay on version 12.04 and do not upgrade to Ubuntu 14 (Trusty Tar). This can take a while.

```
sudo apt-get --yes update && sudo apt-get --yes upgrade && sudo \
	apt-get --yes dist-upgrade && sudo apt-get --yes autoremove
```

Binairies are executed from your local `bin` folder. Create your `~/bin` and add it to your PATH if needed.

```
if ! [[ "$PATH" =~ (:$HOME/bin:|:~/bin:) ]] ; then \
	mkdir -p ~/bin && \
	printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.profile
	fi
```

Reboot.

```
sudo reboot
```

Now we are up to date, and ready to continue the installation.

#### Step 2 - Install required libraries and packages using apt-get
This apt-get oneliner will install most of the important packages we need and takes take of most dependencies as well.

```
sudo apt-get --yes update && sudo apt-get --yes install autoconf \
    automake "build-essential" cvs gimp git "libgtk2.0-dev" \
    "libjpeg-dev" "libopenjpeg-dev" "libopenslide-dev" "libsqlite3-dev" \
    libtool "libxml2-dev" parallel perl "pkg-config" vim wget wmctrl \
    "zbar-tools"
```

Most dependcies are now installed, but we need some more.

#### Step 3 - Install zlib
Install the latest zlib compression libraries. First create and go to the src directory, download and extract zlib.

```
mkdir -p ~/src && cd ~/src && \\
    wget http://zlib.net/zlib-1.2.8.tar.gz -O zlib-1.2.8.tar.gz && \
	tar xzvf zlib-1.2.8.tar.gz && \
	rm zlib-1.2.8.tar.gz
```
Install zlib.

```
cd ~/src/zlib-1.2.8
```
```
./configure && make && sudo make install && make clean
```

#### Step 4 - Install libtiff
Install the latest libtiff library using cvs. When asked for a password, just press enter. The funny thing is, sudo apt-get install libtiff4 does install libtiff 3.9.* We need libtiff 4.* for BigTIFF support.! Download the latest source:

```
mkdir -p ~/cvs && cd ~/cvs
```
```
cvs -d :pserver:cvsanon:@cvs.maptools.org:/cvs/maptools/cvsroot checkout libtiff
```
Install libtiff.

```
cd ~/cvs/libtiff
```
```
./configure && make && sudo make install && make clean
```

#### Step 5 - Install ImageMagick
Download the latest ImageMagick source from there website:

```
mkdir -p ~/src/ && cd ~/src
```
```
wget http://www.imagemagick.org/download/ImageMagick.tar.gz -O ImageMagick.tar.gz && \
	tar xzfv ImageMagick.tar.gz && \
	rm ImageMagick.tar.gz
```

Install ImageMagick.

```
cd ~/src/ImageMagick*
```
```
./configure && make && sudo make install && make clean
```
```
sudo ldconfig /usr/local/lib
```

#### Step 6 - Install openslide
Download the latest version of openslide from github. Pull if already exists; clone if none existing.


```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/openslide/.git ]; then \
		cd ~/git/openslide && git pull; \
	else \
		cd ~/git/ && git clone git://github.com/openslide/openslide.git && \
	fi
```

Install openslide.

```
cd ~/git/openslide
```
```
autoreconf -i
```
```
./configure && make && sudo make install && make clean
```

#### Step 7 - Install bfconvert
Install the latest version of bfconvert:

```
mkdir -p ~/usr && cd ~/usr
```
```
wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
    unzip -o bftools.zip && \
    rm bftools.zip
```
Add symbolic links in `/usr/local/bin/`. Now the BioFormats tools will be availabe in your PATH. Adding the bftools  to your PATH is obligatory for the slideToolkit to find its dependencies.

```
mkdir -p ~/bin/ && ln -s -f -v ~/usr/bftools/bfconvert ~/bin/ && \
    ln -s -f -v ~/usr/bftools/domainlist ~/bin/ && \
    ln -s -f -v ~/usr/bftools/formatlist ~/bin/ && \
    ln -s -f -v ~/usr/bftools/ijview ~/bin/ && \
    ln -s -f -v ~/usr/bftools/mkfake ~/bin/ && \
    ln -s -f -v ~/usr/bftools/showinf ~/bin/ && \
    ln -s -f -v ~/usr/bftools/tiffcomment ~/bin/ && \
    ln -s -f -v ~/usr/bftools/xmlindent ~/bin/ && \
    ln -s -f -v ~/usr/bftools/xmlvalid ~/bin/
```

#### Step 8 - Install datamatrix barcode libraries
Here we install the `dmtx` libraries and binairies. First the libraries:

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/libdmtx/.git ]; then \
		cd ~/git/libdmtx && git pull; \
	else \
		cd ~/git/ && git clone git://libdmtx.git.sourceforge.net/gitroot/libdmtx/libdmtx; \
	fi
```
```
cd ~/git/libdmtx && mkdir -p m4 && autoreconf --force --install
```
```
./configure && make && sudo make install && make clean
```
Now the binairies:

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/dmtx-utils/.git ]; then \
		cd ~/git/dmtx-utils && git pull; \
	else \
		cd ~/git/ && git clone git://git.code.sf.net/p/libdmtx/dmtx-utils; \
	fi
```
```
cd ~/git/dmtx-utils && mkdir -p m4 && autoreconf --force --install
```
```
./configure && make && sudo make install && make clean
```
#### Step 9 - Download the slideToolkit
Download the latest version of the slideToolkit from github. And add it to your PATH.

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/slideToolkit/.git ]; then \
		cd ~/git/slideToolkit && git pull; \
	else \
		cd ~/git/ && git clone https://github.com/bglnelissen/slideToolkit.git; \
	fi
```

Add symbolic links in `~/bin/`. Now the slideToolkit will be availabe in your PATH. Adding the slideToolkit tools to your PATH makes it easier to acces the slideToolkit commands.

```
mkdir -p ~/bin/ && ln -s -f -v ~/git/slideToolkit/slide* ~/bin/
```

#### Step 10 - CellProfiler
Install CellProfiler following instructions on their [website](http://cellprofiler.org/download.shtml).

As root, create a file called /etc/yum.repos.d/cellprofiler.repo with the following contents:

```
[cellprofiler]
name=CellProfiler for CentOS 6
baseurl=http://www.cellprofiler.org/linux/centos6/
enabled=1
gpgcheck=0
```
	
As root:

```
yum install cellprofiler
````
As a regular user, type `cellprofiler` to start CellProfiler. If the DISPLAY environment variable is set, CellProfiler will run in GUI mode.

```
cellprofiler
```


#### Step 11 - Cleanup, restart & you're done!
Fix linked libraries.

```
sudo ldconfig
```
Restart.

```
sudo reboot
```

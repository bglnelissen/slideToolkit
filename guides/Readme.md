Installation instructions & dependency's
============

The slideToolkit is a set of scripts that requires other programs and libraries to run. Here we explain the dependencies and show instructions on how to install these dependencies. The required dependencies can change and might break your curren slideToolkit installation. Please tell us if you run into problems, it is likely we can help you out.

#### Guides:

- [Ubuntu 12.04 installation instructions](#ubuntu_12.04)
- [OS X 10.9 Mavericks](#osx_10.9)

<a name="ubuntu_12.04"></a>
Ubuntu 12.04 - slideToolkit installation instructions
--------------

Here are the installation instructions for Ubuntu 12.04 [LTS](https://wiki.ubuntu.com/LTS).
Ubuntu 12.04 is probably the most documented and most supported version
of Linux available today. I tried to create as few steps as possible
with one-liners that are *easy* to read. You can copy/paste each command, line by line. All
steps run in the Terminal.

```
these `mono-type font` illustrate commands illustrate terminal commands. You can copy & paste these.
```

To make it easier to copy and paste, long commands that stretch over multiple lines are structed as follows:

```
Multiline commands end with a dash \
	indent, and continue on the next line.
```

#### Step 1 - Make shure you have the 'latest & greatest'
The system must be up-to-date. Install updates, answer --yes to everything. This can take a while.

```
sudo apt-get --yes update && sudo apt-get --yes upgrade && sudo \
	apt-get --yes dist-upgrade && sudo apt-get --yes autoremove
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
	automake "build-essential" cvs gimp git "libgtk2.0-dev" "libjpeg-dev" \
	"libopenjpeg-dev" "libopenslide-dev" "libsqlite3-dev" libtool \
	"libxml2-dev" parallel perl "pkg-config" vim wget wmctrl
```

Most dependcies are now installed, but we need some more.

#### Step 3 - Install zlib
Install the latest zlib compression libraries. First create and go to the src directory, download and extract zlib.

```
mkdir -p ~/src && cd ~/src
wget http://zlib.net/zlib-1.2.8.tar.gz -O zlib-1.2.8.tar.gz && \
	tar xzvf zlib-1.2.8.tar.gz && \
	rm zlib-1.2.8.tar.gz
```
Install zlib.

```
cd ~/src/zlib-1.2.8
./configure
make
sudo make install && make clean
```

#### Step 4 - Install libtiff
Install the latest libtiff library using cvs. When asked for a password, just press enter. The funny thing is, sudo apt-get install libtiff4 does install libtiff 3.9.* We need libtiff 4.* for BigTIFF support.! Download the latest source:

```
mkdir -p ~/cvs && cd ~/cvs
export CVSROOT=:pserver:cvsanon@cvs.maptools.org:/cvs/maptools/cvsroot
cvs login # no password, just press enter
cvs checkout libtiff
```
Install libtiff.

```
cd ~/cvs/libtiff
./configure
make
sudo make install && make clean
```

#### Step 5 - Install ImageMagick
Download the latest ImageMagick source from there website:

```
mkdir -p ~/src/ && cd ~/src
wget http://www.imagemagick.org/download/ImageMagick.tar.gz -O ImageMagick.tar.gz && \
	tar xzfv ImageMagick.tar.gz && \
	rm ImageMagick.tar.gz
```

Install ImageMagick.

```
cd ~/cvs/ImageMagick*
./configure
make
sudo make install && make clean
sudo ldconfig /usr/local/lib
```

#### Step 6 - Install openslide
Download the latest version of openslide from github. Pull if already exists; clone if none existing.


```
mkdir -p ~/git/ && cd ~/git
if [ -d ~/git/openslide/.git ]; then \
		echo pull; \
		cd ~/git/openslide && \
		git pull; \
	else \
		echo clone; \
		cd ~/git/ && \
		git clone git://github.com/openslide/openslide.git && \
		cd ~/git; \
	fi
```

Install openslide.

```
cd ~/git/openslide
autoreconf -i
./configure
make
sudo make install && make clean
```

#### Step 7 - Install bfconvert
Install the latest version of bfconvert:

```
mkdir -p ~/usr && cd ~/usr
wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
	unzip -o bftools.zip && \
	rm bftools.zip
printf "\n# Add the bfconvert directory to the PATH \nPATH=\"$HOME/usr/bfconvert:\$PATH\" \n\n" \
	>> ~/.profile
```

#### Step 8 - Download the slideToolkit
Download the latest version of the slideToolkit from github. Pull if already exists; clone if none existing.

```
mkdir -p ~/git/ && cd ~/git
if [ -d ~/git/slideToolkit/.git ]; then \
		cd ~/git/slideToolkit && \
		git pull; \
	else \
		cd ~/git/ && \
		git clone git://github.com/bglnelissen/slideToolkit.git && \
		cd ~/git; \
	fi
```

#### Step 9 - Cleanup, restart & you're done!
Fix linked libraries and restart.

```
sudo ldconfig
sudo reboot
```

<a name="osx_10.9"></a>
OS X 10.9 Mavericks - slideToolkit installation instructions
--------------

Here are the installation instructions for OS X Mavericks. I tried to create as few steps as possible
with one-liners that are *easy* to read. Most of the installation is done with [brew](http://brew.sh) You can copy/paste each command, line by line. For some steps you need administrator privileges. All steps run in the Terminal.

```
these `mono-type font` illustrate commands illustrate terminal commands. You can copy & paste these.
```

To make it easier to copy and paste, long commands that stretch over multiple lines are structed as follows:

```
Multiline commands end with a dash \
	indent, and continue on the next line.
```

#### Step 1 - Make shure you have the 'latest & greatest'
The system must be up-to-date. Go to the Apple menu on the top left, click "Softeware Update...", and click the "Update all" button. If the system asks you if you want to turn on automatic updates, select 'Turn on'. Restart your system if needed.

Now we are up to date, and ready to continue the installation.

#### Step 2 - Install XQuartz, a version of the X.Org X Window System that runs on OS X
XQuartz is needed. Go to [xquartz.macosforge.org](http://xquartz.macosforge.org), download (about 70mb) and install the latest stable version of XQuartz. You can find it under "Quick Download".

On the end of the installation you are asked to log out and log back in, and of course you comply.

#### Step 3 - Install brew, the missing package manager for OS X
We install [brew](http://brew.sh) using the following one-liner. You need administrator rights for the installation. No characters will appear on the screen when you type in your password. Paste the following oneliner in your the terminal.

```
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

When asked if you want to install the "command line developer tools", choose 'Install'. After the "command line developer tools" installation, continue the installation in the Terminal

After a `brew` installation, it is wise to do a `brew doctor` and follow the instructions on the screen.

```
brew doctor
```

Now your `brew` packages manager is good to go.

#### Step 4 - Install packages using brew
We install most packages using brew.

```
brew install wget jpeg libpng libtiff parallel \
    imagemagick --with-libpng --with-libtiff --with-x11 --build-from-source
```

#### Step 5 - Disable parallel bibtex warning
On each run, `parallel` asks you to cite it when you use GNU parallel to process data for publication. To disable this warning you need to run the following command once and follow instructions on the screen. 

```
parallel --bibtex
```

Respect the auther, and please cite when appropriate. 

#### Step 6 - Install slideToolkit
Download and install the latest version of the slideToolkit.

```
cd ~/ \
	wget https://github.com/bglnelissen/slideToolkit/archive/master.zip -O slideToolkit.zip && \
	unzip slideToolkit.zip && \
	rm slideToolkit.zip && \
	mv ~/slideToolkit-master ~/slideToolkit	
```

Add the slideToolkit directory to your path

```
printf "\n# Add the slideToolkit directory to the PATH \
    \nPATH=\"$HOME/slideToolkit:\$PATH\" \n\n" \
	>> ~/.bash_profile
```

#### Step 7 - Reboot
Restart and you're done.
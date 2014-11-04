CentOS 6.6 - slideToolkit installation instructions
============

The slideToolkit is a set of scripts that requires other programs and libraries to run. Here we explain the dependencies and show instructions on how to install these dependencies. The required dependencies can change and might break your curren slideToolkit installation. 

Please tell us if you run into problems, it is likely we can help you out, we have done this before ;)

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

Although we made it easy to just select, copy and paste and run these blocks of code, it is not a good practise to blindly copy and paste commands. Try to be aware about what you are doing. And never, never run `sudo` commands without a good reason to do so.

------------

#### Update and prepare
To make installing easier, we will add the current user to the sudoers file, this makes it possible to run `sudo`. Replace USERNAME with your username.

```
sudo adduser USERNAME sudo
```

The system must be up-to-date. Install updates, answer --yes to everything. Make sure you stay on CentOS version 6.6 as this guide is meant for CentOS 6.6 only. This can take a while.

```
su -c 'yum -y update'
```

Binairies are executed from your local `bin` folder. Create your `~/bin` and add it to your PATH if needed.

```
mkdir -p ~/bin && \
if ! [[ "$PATH" =~ ($HOME/bin:|~/bin:) ]] ; then \
	printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.profile
	fi
```

Now we are up to date, and ready to continue the installation.

#### Install required libraries and packages using apt-get
This apt-get oneliner will install most of the important packages we need and takes take of most dependencies as well.

```
su -c 'yum -y install autoconf automake cmake curl cvs gcc gcc-c++ \
    gimp git libtool openjpeg perl svn vim wget  \
    giflib-devel libjpeg-devel libtiff-devel libpng-devel freetype-devel'
```

# wmctrl
# zbar-tools


#### Install parallel
Install the latest version of GNU Parallel. First create and go to the src directory, then download and extract parallel.

```
mkdir -p ~/src && cd ~/src && \\
    wget http://ftp.gnu.org/gnu/parallel/parallel-latest.tar.bz2 && \
	tar jxf parallel-latest.tar.bz2 && \
	rm parallel-latest.tar.bz2
```

Install parallel

```
cd ~/src/parallel-*
```
```
./configure && make && su -c "make install" && make clean
```

#### Install zlib
Install the latest zlib compression libraries. First create and go to the src directory, then download and extract zlib.

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
./configure && make && su -c "make install" && make clean
```

#### Install libtiff
Install the latest libtiff library using cvs. When `cvs` asks for a password for the anonymous login, just press enter. We need libtiff 4.* for BigTIFF support. First create and go to the cvs directory, then download and extract libtiff.

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
./configure && make && su -c "make install" && make clean
```

#### Install JPEG2000
```
mkdir -p ~/svn && cd ~/svn
```
```
svn checkout http://openjpeg.googlecode.com/svn/trunk/ openjpeg
```
Install openjpeg.

```
cd ~/svn/openjpeg
```

```
cmake . && make && su -c "make install" && make clean
```


#### Install ImageMagick
Download and install the latest version ImageMagick from there website. First create and go to the src directory, then download and extract ImageMagick.

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
./configure && make && su -c "make install" && make clean
```

After the ImageMagick installation we need to examine the libraries, update links and cache where necessary. Else ImageMagick would work properly.

```
sudo ldconfig /usr/local/lib
```

#### Install openslide [openjpeg not found error]
Download the latest version of openslide from github. Pull if already exists; clone if none existing. First create and go to the git directory, then download the source.

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/openslide/.git ]; then \
		cd ~/git/openslide && git pull; \
	else \
		cd ~/git/ && git clone git://github.com/openslide/openslide.git; \
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
./configure && make && su -c "make install" && make clean
```

#### Install bfconvert
Download and install the latest version of bfconvert. First create and go to the usr directory, then download and extract bftools.

```
mkdir -p ~/usr && cd ~/usr
```
```
wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
    unzip -o bftools.zip && \
    rm bftools.zip
```
No need to configure the bftools. We only need to add symbolic links in `~/bin`, this will make the BioFormats availabe within your PATH. Adding the bftools to your PATH is obligatory for the slideToolkit to find its dependencies.

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

#### Install datamatrix barcode libraries [error: dmtx lib not found]
Download and install the latest version of the datamatrix barcode libraries and binairies (`dmtx`) from sourceforge using git. First create and go to the git directory, then download and extract the libraries.

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
Install the datamatrix barcode libraries

```
cd ~/git/libdmtx && mkdir -p m4 && autoreconf --force --install
```
```
./configure && make && su -c "make install" && make clean
```
Now the binairies. First create and go to the git directory, then download and extract the binairies.

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

Install the datamatrix barcode binairies.

```
cd ~/git/dmtx-utils && mkdir -p m4 && autoreconf --force --install
```
```
./configure && make && su -c "make install" && make clean
```
#### Install slideToolkit
Download and install the latest version of the slideToolkit from github. First create and go to the git directory, then download the slideToolkit.

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


#### Install CellProfiler
Instructions for CentOS 6 taken from on [cellprofiler.org](http://www.cellprofiler.org).

Create repository file.

```
mkdir -p /etc/yum.repos.d && \
if ! [[ -f /etc/yum.repos.d/cellprofiler.repo ]] ; then \
    su -c 'printf "\n[cellprofiler]\n\
    name=CellProfiler for CentOS 6\n\
    baseurl=http://www.cellprofiler.org/linux/centos6/\n\
    enabled=1\n\
    gpgcheck=0" > /etc/yum.repos.d/cellprofiler.repo';
    fi
```

```
su -c 'yum install cellprofiler'
```

#### Cleanup, restart & you're done!
Fix linked libraries.

```
sudo ldconfig
```
Restart.

```
sudo reboot
```


OS X slideToolkit installation instructions
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

We have tested slideToolkit on Mac OS X 10.9 Mavericks, OS X 10.10 Yosemite, and OS X 10.11 El Capitan. The only issue is with the `wmctrl` package - please refer to the "Issues" for more information: https://github.com/bglnelissen/slideToolkit/issues/24.

--------------

#### Step 1 - Update and prepare
The system must be up-to-date. Go to the Apple menu on the top left, click "Software Update...", and click the "Update all" button. If the system asks you if you want to turn on automatic updates, select 'Turn on'. Restart your system if needed.

Binairies are executed from your local `bin` folder. By default this folder does not exists and is not present in your PATH. Create your `~/bin` and add it to your PATH if needed.

```
if ! [[ "$PATH" =~ (:$HOME/bin:|:~/bin:) ]] ; then \
	mkdir -p ~/bin && \
	printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.bash_profile
	fi
```

Now we are up to date, and ready to continue the installation.

#### Step 2 - Install XQuartz, a version of the X.Org X Window System that runs on OS X
XQuartz is needed. Go to [xquartz.macosforge.org](http://xquartz.macosforge.org), download and install the latest stable version of XQuartz. You can find it under "Quick Download".

On the end of the installation you are asked to log out and log back in, and of course you comply.

#### Step 3 - Install brew 🍺, the missing package manager for OS X
We install [brew](http://brew.sh) using the following one-liner. You need administrator rights for the installation. No characters will appear on the screen when you type in your password.

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

#### Step 4 - Install required libraries and packages using brew 🍺
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

#### Step 7 - Install slideToolkit
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

We also have to make all the `bftools` available in your path.

```
mkdir -p ~/bin/ && ln -s -f -v ~/usr/bftools/bf.sh ~/bin/
```


#### Step 8 - Install CellProfiler
Install CellProfiler following instructions on their [website](http://cellprofiler.org/download.shtml). Using the downloaded installer, CellProfiler will be installed in the default location (/Applications/CellProfiler).

To make the CellProfiler command line interface (CLI) available, we create a `cellprofiler` script in your `~/bin` folder. This scripts links to CellProfiler installed in your /Applications folder.

```
printf '#!/bin/bash\n# run cellprofiler from CLI\n/Applications/CellProfiler.app/Contents/MacOS/CellProfiler "$@"\n' \
    > ~/bin/cellprofiler && chmod 755 ~/bin/cellprofiler

```

#### Step 9 - Reboot
Reboot your system and you're done.

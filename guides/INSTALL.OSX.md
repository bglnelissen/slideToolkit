macOS and OS X 10.9+ - slideToolkit installation instructions
============

The **slideToolKit** is a set of scripts that requires other programs and libraries to run. Here we explain the dependencies and show instructions on how to install these dependencies. The required dependencies can change and might break your current slideToolkit installation.

We have tested **slideToolKit** on CentOS6, CentOS7, OS X Mountain Lion+ (version 10.8.[x]+), macOS Sierra (version 10.12.[x]), macOS High Sierra (version 10.13.[x]), macOS Mojave (version 10.14.[x]), and macOS Catalina (version 10.15.[x]).

Please tell us if you run into problems, it is likely we can help you out - we have done this before. ;)

--------------

#### Some installation basics

We tried to create as few steps as possible with one-liners that are *easy* to read. Most of the installation is done using the commandline. You can copy/paste each example command, per block of code. For some steps you need administrator privileges. Follow the steps in consecutive order.

```
these `mono-type font` illustrate commands illustrate terminal commands. You can copy & paste these.
```

To make it easier to copy and paste, long commands that stretch over multiple lines are structered as follows:

```
Multiline commands end with a dash \
	indent 4 spaces, and continue on the next line. \
	Copy & paste these whole blocks of code.
```

Although we made it easy to just select, copy and paste and run these blocks of code, it is not a good practise to blindly copy and paste commands. Try to be aware about what you are doing. And never, never run `sudo` commands without a good reason to do so.

--------------

#### Step 1 - Update and prepare.
The system must be up-to-date. Go to the Apple menu on the top left, click "Software Update...", and click the "Update all" button. If the system asks you if you want to turn on automatic updates, select 'Turn on'. Restart your system if needed.

Binairies are executed from your local `bin` folder. By default this folder does not exists and is not present in your PATH. Create your `~/bin` and add it to your PATH if needed.

```
if ! [[ "$PATH" =~ (:$HOME/bin:|:~/bin:) ]] ; then \
	mkdir -p ~/bin && \
	printf "\n# Add ~/bin to your PATH\nexport PATH=\"~/bin:\$PATH\" \n" >> ~/.bash_profile
	fi
```

Now we are up to date, and ready to continue the installation.

#### Step 2 - Install XQuartz, a version of the X.Org X Window System that runs on OS X.
XQuartz is needed. Go to [xquartz.macosforge.org](http://xquartz.macosforge.org), download and install the latest stable version of XQuartz. You can find it under "Quick Download".

On the end of the installation you are asked to log out and log back in, and of course you comply.

#### Step 3 - Install brew 🍺, the missing package manager for OS X.
We install [brew](http://brew.sh) using the following one-liner. You need administrator rights for the installation. No characters will appear on the screen when you type in your password.

```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
P.S. You can check out more handy Homebrew repositories here: https://github.com/Homebrew.

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

#### Step 4 - Install required libraries and packages using brew 🍺.
We install most packages using brew.

```
brew install automake wget jpeg libpng libtiff parallel openslide wmctrl zbar
```

#### Step 5 - Install `ImageMagick`.
First, we will uninstall *all* previous installations of `ImageMagick`, before we build it from source. 

```
brew uninstall --ignore-dependencies --force imagemagick
```

Now, we are ready to install the latest `ImageMagick` from brew 🍺 and from _source_, because otherwise `slideEMask` will not work. 

```
brew install -s imagemagick 
```

Note: We need ImageMagick 7+ (IM7) which is ported from ImageMagick 6 (IM6) and has an important change with respect to images. It has improved with respect to high dynamic range imaging (HDRI) by default. The default in IM7 is to update the RGBA channels. Previously in IMv6, the default was RGB. To handle this `slide2Tiles`, which uses `convert` from IM7 was edited to handle these channels: 

Old IM6 version:

```
convert "${S}[${LAYER}]" \( "${M}" -fuzz 99% -transparent white -scale ${dimensionsslide} -negate \) -composite -fuzz 3% -trim +repage -bordercolor white -border 30x30 +repage "${buffer}"
```


New IM7 version:

```
convert "${S}[${LAYER}]" \( "${M}" -fuzz 99% -transparent white -scale ${dimensionsslide} -channel RGB -negate \) -composite -fuzz 3% -trim +repage -bordercolor white -border 30x30 +repage "${buffer}"
```

For reference check [this link](https://imagemagick.org/script/porting.php).

#### Step 6 - Install the bioformat tools.
Install the latest version of BioFormats, including `bfconvert`.

```
mkdir -p ~/usr
```
```
cd ~/usr && wget http://downloads.openmicroscopy.org/latest/bio-formats5/artifacts/bftools.zip && \
	unzip -o bftools.zip && \
	rm bftools.zip
```
Add symbolic links in `~/bin/`. Now the BioFormats tools will be availabe in your PATH. Adding the bftools  to your PATH is obligatory for the **slideToolKit** to find its dependencies.

```
mkdir -p ~/bin/ && \
	ln -s -f -v ~/usr/bftools/bfconvert ~/bin/ && \
	ln -s -f -v ~/usr/bftools/domainlist ~/bin/ && \
	ln -s -f -v ~/usr/bftools/formatlist ~/bin/ && \
	ln -s -f -v ~/usr/bftools/ijview ~/bin/ && \
	ln -s -f -v ~/usr/bftools/mkfake ~/bin/ && \
	ln -s -f -v ~/usr/bftools/showinf ~/bin/ && \
	ln -s -f -v ~/usr/bftools/tiffcomment ~/bin/ && \
	ln -s -f -v ~/usr/bftools/xmlindent ~/bin/ && \
	ln -s -f -v ~/usr/bftools/xmlvalid ~/bin/
```

#### Step 7 - Install datamatrix barcode libraries.
Install the latest version of `libdmtx`, including `dmtxread`. First we install the libraries:

```
brew install libdmtx
```

Luckily, `dmtx-utils` was updated to work with both `ImageMagick 6+` and `ImageMagick 7+`, and thus it was restored from `homebrew/boneyard`. See also: https://github.com/Homebrew/homebrew-core/pull/10693 and https://github.com/dmtx/dmtx-utils/issues/2. Now we can install it the easy way, using brew 🍺. 

```
brew install dmtx-utils
```

The dmtx and libdmtx binairies are installed in `/usr/local/bin`. This is the folder `brew` uses for its installations and should already be in your PATH.

#### Step 8 - Install slideToolkit.
Download and install the latest version of the **slideNormalize** from GitHub. First create and go to the git directory, then download the **slideToolKit**.

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/slideToolKit/.git ]; then \
		cd ~/git/slideToolKit && git pull; \
	else \
		cd ~/git/ && git clone https://github.com/swvanderlaan/slideToolKit.git; \
	fi
```

Add symbolic links in `~/bin/`. Now the **slideToolKit** will be availabe in your PATH. Adding the **slideToolKit** tools to your PATH makes it easier to acces the slideToolkit commands.

```
mkdir -p ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slide2Tiles ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideConvert ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideDirectory ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideEMask ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideInfo ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideJobsCellProfiler ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideMask ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideMacro ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideQuantify ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideQuantifyLocal ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideRename ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideReset ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideSQLheader ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideThumb ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideExtract.py ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideInfo.py ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideMacro.py ~/bin/ && \
	ln -s -f -v ~/git/slideToolKit/slideThumb.py ~/bin/
 
```

#### Step 9 - Instal NDPITools

Some pathology scanners produce proprietary `NDPI`-files. These are almost similar to `TIF`, but with some differences. To be able to run _slideToolKit_ and _CellProfiler_ we need to install a small package `NDPITools` to convert `NDPI`-files to `TIF`. 

Simply go to the [NDPITools website](https://www.imnc.in2p3.fr/pagesperso/deroulers/software/ndpitools/) and following the instructions for macOS.

#### Step 10 - Install CellProfiler, we prefer version 2.2.0.
Install `CellProfiler version 2.2.0` following instructions on their [website](http://cellprofiler.org/download.shtml). Using the downloaded installer, CellProfiler will be installed in the default location (/Applications/CellProfiler).

To make the CellProfiler command line interface (CLI) available, we create a `cellprofiler` script in your `~/bin` folder. This scripts links to CellProfiler installed in your /Applications folder.

```
printf '#!/bin/bash\n# run cellprofiler from CLI\n/Applications/CellProfiler.app/Contents/MacOS/CellProfiler "$@"\n' \
    > ~/bin/cellprofiler && chmod -v 0755 ~/bin/cellprofiler

```

##### Alternative versions of CellProfiler
We prefer version 2.2.0 because this version works best on our _high-performance computing cluster_. That said: one could easily install the latest version by simply changing the version number of CellProfiler in the command above, if needed. For example:

```
printf '#!/bin/bash\n# run cellprofiler from CLI\n/Applications/CellProfiler-3.1.8.app/Contents/MacOS/cp "$@"\n' \
    > ~/bin/cellprofiler && chmod -v 0755 ~/bin/cellprofiler
```

_Note: an alternative installation instruction for CellProfiler could be found [here](https://github.com/CellProfiler/CellProfiler/wiki/Source-installation-%28OS-X-and-macOS%29)_


> Disclaimer: we have not fully tested our workflow and slideToolKit with newer versions of CellProfiler. Presumably `pipelines` need to be edited to fit the new version.

#### Step 11 - Reboot.
Reboot your system and you're done.

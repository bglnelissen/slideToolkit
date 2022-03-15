CentOS 7 ~ Anaconda-version - slideToolkit installation instructions
============

The slideToolkit is a set of scripts that requires other programs and libraries to run. Here we explain the dependencies and show instructions on how to install these dependencies. The required dependencies can change and might break your current slideToolkit installation. 

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

NOTE: these instructions are for CentOS7 on a high-performance computer cluster, such as the HPC at the UMC Utrecht.

------------

## Anaconda version

The HPC is managed and user do not normally have admin rights. Therefore it is advised to install a distribution of `anaconda`.

### Step 1: check what is available on the system
Let's first check whether some packages are installed already.

```
for PACK in curl cvs gcc gcc-c++ gimp git libtool openjpeg perl svn vim wget giflib-devel libjpeg-devel libtiff-devel libpng-devel freetype-devel; do echo "* checking [ "$PACK" ]...."; command -v "$PACK"; echo "---------"; echo ""; done
```

### Step 2: installation anaconda
We require `anaconda` to have full control on the installation of required libraries and packages for `slideToolKit`.

If `anaconda` is available, make sure it is up-to-date.

```
conda update -n base conda
```

If `anaconda` is not available, you can grab a [link here](https://www.anaconda.com/products/individual#linux). Next, execute the following two lines in the root folder where you want `anaconda` to be installed, e.g. `/hpc/local/CentOS7/dhl_ec/software/`:

```
wget https://repo.anaconda.com/archive/Anaconda3-2021.05-Linux-x86_64.sh
```

```
bash Anaconda3-2021.05-Linux-x86_64.sh
```

And follow the instructions. 

If you don't want conda to be loaded on startup, you can execute the following command.

```
conda config --set auto_activate_base false
```

And don't forget to cleanup afterwards.

```
rm -v Anaconda3-2021.05-Linux-x86_64.sh
```

### Step 4: make a module for anaconda

You can create a [`modulefile`](https://lmod.readthedocs.io/en/latest/015_writing_modules.html) to make loading this particular `anaconda` installment easy and fun.

Create a text file with the following contents.

```
help(
[[ anaconda(version 3-8.202105) Anaconda, containing CellProfiler 4.1.3
]])

whatis("anaconda(version 3-8.202105) Anaconda, containing CellProfiler 4.1.3")

local version = "3-8.202105"

local base = "/hpc/local/$MY_DISTRO/$MY_GROUP/software/Anaconda3_2021_05"

conflict("anaconda")

prepend_path("PATH", pathJoin(base, "bin"))

```

Your administrator can tell you precisely where these `modulefiles` should be stored. In our case, they are in a folder `/hpc/local/CentOS7/dhl_ec/etc/modulefiles/anaconda` for our group. Save the text-file as `3-8.2021.05.lua` in the `modulesfiles`-directory.

Restart your shell:

```
source $HOME/.bashrc
source $HOME/.bash_profile
```

You can now load your fresh `anaconda` installation:

```
module load anaconda/3-8.202105
```


### Step 5: installation required packages


```
conda install -c anaconda automake cmake enum34 requests libtiff libpng freetype zlib numpy scipy cython 
```


```
conda install -c c4aarch64 autoconf
```


```
conda install -c conda-forge zbar openjpeg giflib libjpeg-turbo wmctrl parallel pylibdmtx imagemagick matplotlib gtk3 
```


```
conda install -c bioconda bftools java-jdk
```


### Step 6: installation slideToolkit
Download and install the latest version of the slideToolkit from github. First create and go to the git directory, then download the slideToolkit.

```
mkdir -p ~/git/ && cd ~/git
```
```
if [ -d ~/git/slideToolkit/.git ]; then \
		cd ~/git/slideToolkit && git pull; \
	else \
		cd ~/git/ && git clone https://github.com/swvanderlaan/slideToolKit.git; \
	fi
```

Add symbolic links in `~/bin/`. Now the slideToolkit will be availabe in your PATH. Adding the slideToolkit tools to your PATH makes it easier to acces the slideToolkit commands.

```
mkdir -p ~/bin/ && ln -s -f -v ~/git/slideToolkit/slide* ~/bin/
```


### Step 7: make a module for slideToolKit

Let's create a `modulefile` to make loading `slideToolKit` easy and fun.

Create a text file with the following contents.

```
help(
[[ slideToolKit(version 1.0) slideToolKit
]])

whatis("slideToolKit(version 1.0) slideToolKit")

local version = "1.0"

local base = "/hpc/local/$MY_DISTRO/$MY_GROUP/software/slideToolKit/" .. version 

conflict("slideToolkit")

prepend_path("PATH", base)

load("gnu-parallel/20170122")
prereq("gnu-parallel/20170122")

load("zlib/1.2.8")
prereq("zlib/1.2.8")

load("imagemagick/6.9.3-10")
prereq("imagemagick/6.9.3-10")

load("openslide/3.4.1")
prereq("openslide/3.4.1")

load("libdmtx/0.7.4")
prereq("libdmtx/0.7.4")

load("dmtx-utils/0.7.4")
prereq("dmtx-utils/0.7.4")

load("graphicsmagick/1.3.26")
prereq("graphicsmagick/1.3.26")

```

Save the text-file as `/hpc/local/CentOS7/dhl_ec/etc/modulefiles/slidetoolkit/version1.0.lua` in the `modulesfiles`-directory.

Restart your shell:

```
source $HOME/.bashrc
source $HOME/.bash_profile
```

You can now load your fresh `slideToolKit` installation:

```
module load slideToolKit/version1.0
```


### Step 8: installation CellProfiler

Follow these instructions to install [CellProfiler](https://github.com/CellProfiler/CellProfiler/wiki/Source-installation-(Linux)).

[instructions forthcoming]



## Cleanup, restart & you're done!
Source your `bash_profile`.

```
source ~/.bash_profile
```

And make sure you load the new modules:

```
module load anaconda/3-8.202105 slideToolKit
```

-------
## To do

- [x] add description on installation `anaconda`.
- [x] add description on how to create `anaconda` module.
- [x] add description on how to install required packages for `anaconda` and `slideToolKit`.
- [x] add description on how to create `slideToolKit` module.
- [.] add description on how to install `cellprofiler`.
- [x] update manual instructions .





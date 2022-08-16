#!/bin/bash

#
# Description: Compare two images with ImageMagick's compare function.
#
# https://softwarerecs.stackexchange.com/questions/9774/command-line-tool-to-check-whether-two-images-are-exactly-the-same-graphically

# Description:
# This script starts up the slideToolKit-CP4 Anaconda3 environment. Next it will extract
# slide-macro images from each .ndpi-file present in a given directory. Lastly it will 
# take a list of studynumbers/slidenumbers to 

# 
# The MIT License (MIT)
# Copyright (c) 2022, Sander W. van der Laan, UMC Utrecht, Utrecht, the Netherlands.
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# 

### Creating display functions
### Setting colouring
NONE='\033[00m'
BOLD='\033[1m'
ITALIC='\033[3m'
OPAQUE='\033[2m'
FLASHING='\033[5m'
UNDERLINE='\033[4m'

RED='\033[01;31m'
GREEN='\033[01;32m'
YELLOW='\033[01;33m'
PURPLE='\033[01;35m'
CYAN='\033[01;36m'
WHITE='\033[01;37m'
### Regarding changing the 'type' of the things printed with 'echo'
### Refer to: 
### - http://askubuntu.com/questions/528928/how-to-do-underline-bold-italic-strikethrough-color-background-and-size-i
### - http://misc.flogisoft.com/bash/tip_colors_and_formatting
### - http://unix.stackexchange.com/questions/37260/change-font-in-echo-command

### echo -e "\033[1mbold\033[0m"
### echo -e "\033[3mitalic\033[0m" ### THIS DOESN'T WORK ON MAC!
### echo -e "\033[4munderline\033[0m"
### echo -e "\033[9mstrikethrough\033[0m"
### echo -e "\033[31mHello World\033[0m"
### echo -e "\x1B[31mHello World\033[0m"

function echobold { #'echobold' is the function name
    echo -e "${BOLD}${1}${NONE}" # this is whatever the function needs to execute, note ${1} is the text for echo
}
function echoitalic { 
    echo -e "${ITALIC}${1}${NONE}" 
}
function echocyan { 
    echo -e "${CYAN}${1}${NONE}" 
}

function echonooption { 
    echo -e "${OPAQUE}${RED}${1}${NONE}"
}

# errors
function echoerrorflash { 
    echo -e "${RED}${BOLD}${FLASHING}${1}${NONE}" 
}
function echoerror { 
    echo -e "${RED}${1}${NONE}"
}

# errors no option
function echoerrornooption { 
    echo -e "${YELLOW}${1}${NONE}"
}
function echoerrorflashnooption { 
    echo -e "${YELLOW}${BOLD}${FLASHING}${1}${NONE}"
}

### MESSAGE FUNCTIONS
script_copyright_message() {
	echo ""
	THISYEAR=$(date +'%Y')
	echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echo "+ The MIT License (MIT)                                                                                 +"
	echo "+ Copyright (c) 2022-${THISYEAR} Sander W. van der Laan                                                        +"
	echo "+                                                                                                       +"
	echo "+ Permission is hereby granted, free of charge, to any person obtaining a copy of this software and     +"
	echo "+ associated documentation files (the \"Software\"), to deal in the Software without restriction,         +"
	echo "+ including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, +"
	echo "+ and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, +"
	echo "+ subject to the following conditions:                                                                  +"
	echo "+                                                                                                       +"
	echo "+ The above copyright notice and this permission notice shall be included in all copies or substantial  +"
	echo "+ portions of the Software.                                                                             +"
	echo "+                                                                                                       +"
	echo "+ THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT     +"
	echo "+ NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND                +"
	echo "+ NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES  +"
	echo "+ OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN   +"
	echo "+ CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.                            +"
	echo "+                                                                                                       +"
	echo "+ Reference: http://opensource.org.                                                                     +"
	echo "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
}

script_arguments_error() {
	echoerror "$1" # ERROR MESSAGE
	echoerror "- Argument #1  -- slidenumber with stain; only 1 slidenumber is permitted. For example, AE4653.CD3."
	echoerror ""
	echoerror "An example command would be: slideCompare [arg1: AE4653.CD3]"
	echoerror ""
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	# The wrong arguments are passed, so we'll exit the script now!
	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                    slideCompare: compare images"
echo ""
echoitalic "* Written by  : Sander W. van der Laan"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2022-08-16"
echoitalic "* Version     : 1.0.0"
echo ""
echoitalic "* Description : This script will compare two images with ImageMagick's compare "
echoitalic "                function."
echoitalic "                This is SLURM based."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo ""
### REQUIRED | GENERALS	
IMG_FILE="$1" # Depends on arg1

### START of if-else statement for the number of command-line arguments passed ###
if [[ $# -lt 1 ]]; then 
	echo "Oh, computer says no! Number of arguments found \"$#\"."
	script_arguments_error "You must supply correct (number of) arguments when running *** slideCompare ***!"
		
else
	
	# Reference
	# https://stackoverflow.com/questions/8903239/how-to-calculate-time-elapsed-in-bash-script
	SECONDS=0
	# do some work

	# checking if masks exist - if so, skip this script
	if [ -f ${IMG_FILE}.diff.png ]; then 
		echo "..... This image was already compared as the [ ${IMG_FILE}.diff.png] already exists - moving on."
		exit 1
	fi

	### Loading required modules
	### Loading the CellProfiler-Anaconda3.8 environment
	### You need to also have the conda init lines in your .bash_profile/.bashrc file
	echo "..... > loading required anaconda environment containing the slideToolKit-CellProfiler4.1.3 installation..."
	eval "$(conda shell.bash hook)"
	conda activate cp4
	SLIDEMACRO="/hpc/local/CentOS7/dhl_ec/software/slideToolKit/slideMacro.py"
	
	echo "Masking and creating a tile-crossed image from original image-file."
	
	if [ -f ${IMG_FILE}.*ndpi ]; then
		echo "The image-file is a NDPI and small macro images will be created for comparing."
		
		echo "\n* creating macro-files\n"
		python $SLIDEMACRO --input ${IMG_FILE}.*ndpi -l 7 -v

		echo "\n* comparing macro-images.\n"
		compare_result=$(magick compare -metric AE ${IMG_FILE}.macro.png ${IMG_FILE}.v2.macro.png ${IMG_FILE}.diff.png 2>&1);
	
		if [ "${compare_result}" != '0' ]; then
				echo "ERROR. ImageMagick determined [ ${compare_result} ] incorrect pixels in slide ${IMG_FILE}. These images are not the same. Please manually inspect the original images (.ndpi/.TIF)";
		fi
	elif [ -f *.tif ]; then 
		echo "The image-file is a .tif. AT THE MOMENT ONLY WORKS FOR NDPI - EXITING"
		exit 1 
	elif [ -f *.TIF ]; then 
		echo "The image-file is a .TIF. AT THE MOMENT ONLY WORKS FOR NDPI - EXITING"
		exit 1 
	else
		echoerrorflash "*** ERROR *** Something is rotten in the City of Gotham; most likely a typo. Double back, please. 
		[image-extension not recognized, should be 'ndpi', 'tif' or 'TIF']
		AT THE MOMENT ONLY WORKS FOR NDPI"
		exit 1 
	fi

	echo "..... Masking successfully finished."

	duration=$SECONDS
	echo "[ $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed ]"


### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message


#!/bin/bash
#
# Description: Creates masks for images using slideEMask as part of a slideQuantify
#              job-session.
# 
# The MIT License (MIT)
# Copyright (c) 2014-2021, Bas G.L. Nelissen, Sander W. van der Laan, 
# UMC Utrecht, Utrecht, the Netherlands.
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
	echo "+ Copyright (c) 2016-${THISYEAR} Sander W. van der Laan                                                        +"
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
	echoerror "- Argument #1   -- path_to ExpressHist directory, e.g. /hpc/local/CentOS7/dhl_ec/software/ExpressHIST/."
	echoerror "- Argument #2   -- Content threshold. The percentage of tissue that should be present at the minimum in a given tile, e.g. 0.5 (5%). [default: 0.5]"
	echoerror "- Argument #3   -- Patch size. Size of the tiles in pixels, e.g. 512 indicates a tile of 512x512; slideToolKit was tested using patches of 2000x2000. [default: 2000]"
	echoerror "- Argument #4   -- Down-sampling. Down-sampling number, to indicate the magnification to use, e.g. with a maximum magnification of 40x, a 2 indcates a downsample to 20x. [default: 2]"
	echoerror "- Argument #5   -- Masking method to apply. Options are otsu, adaptive, or graph (segmentation based). [default: adaptive]"
	echoerror ""
	echoerror "An example command would be: slideQuantify_1_expresshist_mask [arg1: /hpc/local/CentOS7/dhl_ec/software/ExpressHIST/] [arg2: 0.5] [arg3: 2000] [arg4: 2] [arg5: adaptive]"
	echoerror ""
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	# The wrong arguments are passed, so we'll exit the script now!
	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                    slideQuantify: ExpressHIST Masking"
echo ""
echoitalic "* Written by  : Sander W. van der Laan; Yipei Song; "
echoitalic "                Craig Glastonbury"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2023-02-06"
echoitalic "* Version     : 1.0.2"
echo ""
echoitalic "* Description : This script will start the masking of images for "
echoitalic "                slideToolKit analyses; masking can be adaptive, otsu, graph"
echoitalic "                segmentation based."
echoitalic "                This is SLURM based."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo ""
### REQUIRED | GENERALS	
EXPRESSHIST="$1" # Depends on arg1
CONTENTTHRESHOLD="$2" # Depends on arg2
PATCHSIZE="$3" # Depends on arg3
OUTPUTDOWN="$4" # Depends on arg4
MASKMETHOD="$5" # Depends on arg5

### START of if-else statement for the number of command-line arguments passed ###
if [[ $# -lt 1 ]]; then 
	echo "Oh, computer says no! Number of arguments found \"$#\"."
	script_arguments_error "You must supply correct (number of) arguments when running *** slideQuantify_1_expresshist_mask ***!"
		
else
	
	# Reference
	# https://stackoverflow.com/questions/8903239/how-to-calculate-time-elapsed-in-bash-script
	SECONDS=0
	# do some work

	# checking if masks exist - if so, skip this script
	if [ -f mask_*.png ]; then 
		echo "..... Masked images already exists - moving on."
		exit 
	fi

	### loading required modules
	### Loading the CellProfiler-Anaconda3.8 environment
	### You need to also have the conda init lines in your .bash_profile/.bashrc file
	echo "..... > loading required anaconda environment containing the CellProfiler installation..."
	eval "$(conda shell.bash hook)"
	conda activate cp4

	echo "Masking and creating a tile-crossed image from original image-file."
	
	if [ -f *.ndpi ]; then
		echo "The image-file is a NDPI and will be converted to .tif before masking."

		python3 $EXPRESSHIST/pyhist.py --content-threshold $CONTENTTHRESHOLD \
		--patch-size $PATCHSIZE --output-downsample $OUTPUTDOWN --info "verbose" \
		--method "$MASKMETHOD" \
		--save-mask --save-tilecrossed-image *.ndpi

	elif [ -f *.tif ]; then 
		echo "The image-file is a (NDPI-converted) .tif."
		
		python3 $EXPRESSHIST/pyhist.py --content-threshold $CONTENTTHRESHOLD \
		--patch-size $PATCHSIZE --output-downsample $OUTPUTDOWN --info "verbose" \
		--method "$MASKMETHOD" \
		--save-mask --save-tilecrossed-image *.tif

	elif [ -f *.TIF ]; then 
		echo "The image-file is a .TIF."

		python3 $EXPRESSHIST/pyhist.py --content-threshold $CONTENTTHRESHOLD \
		--patch-size $PATCHSIZE --output-downsample $OUTPUTDOWN --info "verbose" \
		--method "$MASKMETHOD" \
		--save-mask --save-tilecrossed-image *.TIF

	else
		echoerrorflash "*** ERROR *** Something is rotten in the City of Gotham; most likely a typo. Double back, please. 
		[image-extension not recognized, should be 'ndpi', 'tif' or 'TIF']"
		exit 1 
	fi

	echo "..... Masking successfully finished."

	duration=$SECONDS
	echo "[ $(($duration / 60)) minutes and $(($duration % 60)) seconds elapsed ]"


### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message


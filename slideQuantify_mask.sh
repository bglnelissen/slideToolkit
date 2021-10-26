#!/bin/bash

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
	echoerror "- Argument #1  -- eMask threshold. A smaller number is less stringent, best results are obtained using, e.g. '210'."
	echoerror ""
	echoerror "An example command would be: slideQuantify_mask [arg1: 210]"
	echoerror ""
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	# The wrong arguments are passed, so we'll exit the script now!
	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                          slideQuantify: Masking"
echo ""
echoitalic "* Written by  : Sander W. van der Laan; Tim Bezemer; Tim van de Kerkhof"
echoitalic "                Yipei Song"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2021-09-02"
echoitalic "* Version     : 2.0.3"
echo ""
echoitalic "* Description : This script will start the masking of images for slideToolKit"
echoitalic "                analyses."
echoitalic "                This is SLURM based."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo ""
### REQUIRED | GENERALS	
EMASKTHRESHOLD="$1" # Depends on arg1

### START of if-else statement for the number of command-line arguments passed ###
if [[ $# -lt 1 ]]; then 
	echo "Oh, computer says no! Number of arguments found \"$#\"."
	script_arguments_error "You must supply correct (number of) arguments when running *** slideQuantify_mask ***!"
		
else

	# checking if masks exist - if so, skip this script
	if [[ -s *mask.png ]] 
	then 
		echo "..... Masked images already exists - moving on."
		exit 
	fi

	# loading required modules 
	module load anaconda/3-8.2021.05
	module load slideToolKit
	module load ndpitools

	mkdir -pv magick-tmp
	export MAGICK_TMPDIR=$(pwd)/magick-tmp
	export TMPDIR=$(pwd)/magick-tmp

	if [ -f *.ndpi ]; then
		echo "The image-file is a NDPI and will be converted to .tif before masking."
		if [ -f *.ndpi ]; then  
			ndpisplit -x20 -z0 *.ndpi; 
		fi
		slideMask --layer 0 -f *.tif;

	elif [ -f *.tif ]; then 
		echo "The image-file is a (NDPI-converted) .tif."
		slideMask --layer 0 -f *.tif;

	elif [ -f *.TIF ]; then 
		echo "The image-file is a .TIF."
		# layer 3 is 20x Roche scanner
		slideMask --layer 3 -f *.TIF;

	else
		echoerrorflash "*** ERROR *** Something is rotten in the City of Gotham; most likely a typo. Double back, please. 
		[image-extension not recognized, should be 'ndpi', 'tif' or 'TIF']"
		exit 1 
	fi

	# running slideMask on the macro
	for MACRO in $(ls *.macro.*); do 
		echo "Running slideEMask on the macro-images."
		slideEMask -f ${MACRO} -t ${EMASKTHRESHOLD}; 
	
	done

	# removing temporary files
	echo "..... Removing temporary directory."
	rm -rfv magick-tmp

	echo "..... Masking successfully finished"
	
### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message


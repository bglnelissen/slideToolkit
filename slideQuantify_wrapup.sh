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
	echoerror "- Argument #1  -- name of the stain as it appears in the filenames, e.g. FIBRIN."
	echoerror "- Argument #2  -- Random sample. A number to indicate the number of overlay-images after analysis to keep, e.g. '20'."
	echoerror ""
	echoerror "An example command would be: slideQuantify_wrapup [arg1: STAIN] [arg2: RANDOM_SAMPLE] "
	echoerror ""
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	# The wrong arguments are passed, so we'll exit the script now!
	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                           slideQuantify: Wrap Up"
echo ""
echoitalic "* Written by  : Sander W. van der Laan; Tim Bezemer; Tim van de Kerkhof"
echoitalic "                Yipei Song"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2021-09-02"
echoitalic "* Version     : 2.0.3"
echo ""
echoitalic "* Description : This script will start the wrap up of a slideToolKit analysis."
echoitalic "                This is SLURM based."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo ""
### REQUIRED | GENERALS	
STAIN="$1" # Depends on arg1
OUTPUTFILENAME=${STAIN}_slides.txt
RANDOM_SAMPLE="$2" # Depends on arg2
# STAIN = "CD34"
# OUTPUTFILENAME = "CD34slides.txt"

# Set slideToolKit DIRECTORY
SLIDETOOLKITDIR="/hpc/local/CentOS7/dhl_ec/software/slideToolKit"

### START of if-else statement for the number of command-line arguments passed ###
if [[ $# -lt 2 ]]; then 
	echo "Oh, computer says no! Number of arguments found \"$#\"."
	script_arguments_error "You must supply correct (number of) arguments when running *** slideQuantify_wrapup ***!"
		
else
	
	### DEBUG
	### SBATCH --output=slidemask_out_%j.log     # Standard output and error log
	
	# Randomly grab x (10) overlay images, and remove the rest
# 	ls cp_output/*.png | shuf -n $(expr $(ls cp_output/*.png | wc -l) - $RANDOM_SAMPLE) | xargs rm;

	# Collecting all the data
	echo "..... Creating [ results.txt ] and collecting data."
	echo 'SampleID Slide_number Stain Counts_per_Tissue_area' > results.txt;
	
	# Moving into the cellprofiler output directory for the given $SLIDE_NUM
	cd cp_output;

	# parsing SLIDE_NUM "$PWD"
	# cut on . (period), output is 1
	SLIDE_NUM=$(basename "$PWD")
	SAMPLE_NUM=$(basename "$PWD") | cut -d'.' -f1
	### DEBUG
	### echo "Original slide number: $SLIDE_NUM"
	### echo "Sample number: $SAMPLE_NUM"
	SCRIPT_NAME="Colsums_${STAIN}.R"
	
	echo $SAMPLE_NUM $SLIDE_NUM $STAIN $(Rscript $SLIDETOOLKITDIR/utilities/$SCRIPT_NAME $STAIN $OUTPUTFILENAME) >> ../results.txt;
	### we used to Gzip
	### gzip -v ../results.txt;
	head ../results.txt
	cat ../results.txt | wc -l
	
	# moving up to the $SLIDE_NUM directory again
	cd ..
	
	echo "..... Removing tiling directory and its contents.";
	# Randomly grab x (50) overlay images, and remove the rest
# 	ls *tiles/*.png | shuf -n $(expr $(ls *tiles/*.png | wc -l) - $RANDOM_SAMPLE) | xargs rm;
# 	rm -rfv *tiles/;

	if [ -f *.ndpi ]; then 
		echo "..... Removing intermediate tif- & png-files converted from NDPI-files.";
# 		rm -v *x40*.tif; 
# 		rm -v *x40*.png; 

	fi;

	echo "..... Removing list of files to process.";
# 	rm -v files2cp.txt;
	
	echo "..... Gzipping result files.";
	gzip -vf cp_output/${STAIN}*.gct;
	gzip -vf cp_output/${STAIN}*.csv;
	

### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message


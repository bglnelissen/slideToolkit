#!/bin/bash
#
# It is good practice to properly name and annotate your script for future reference for
# yourself and others. Trust me, you'll forget why and how you made this!!!

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
	echoerror "- Argument #1  -- name of the recode file which contains two columns (old and new name) WITHOUT header."
	echoerror "- Argument #2  -- (the path to) the images"
	echoerror ""
	echoerror "An example command would be: rename.files.sh [arg1: rename.files.txt] [arg2: some/dir/here] "
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  	# The wrong arguments are passed, so we'll exit the script now!
  	exit 1
}

echobold "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                              rename.files"
echobold ""
echobold "* Written by  : Sander W. van der Laan"
echobold "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echobold "* Last update : 2021-11-16"
echobold "* Version     : 1.2"
echobold ""
echobold "* Description : This script will rename files based on a two arguments and a."
echobold "                file containing the old and new names."
echobold ""
echobold "* Example input: ./rename.files.sh recode.txt inputdir"
echobold "* Example [ recode.txt ]"
echobold "AE1149.T06-25428_A.SMA.20141016.ndpi	AE1149.T06-25428.A.SMA.20141016.ndpi"
echobold "AE1419.T06-24242_A.SMA.20141016.ndpi	AE1419.T06-24242.A.SMA.20141016.ndpi"
echobold "AE1556.T07-13869_A.SMA.20141016.ndpi	AE1556.T07-13869.A.SMA.20141016.ndpi"
echobold ""
echobold "Today's: "$(date)
TODAY=$(date +"%Y%m%d")
echobold "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo ""
echo "------------------------------------------------------------------------------------"
echobold "Checking input."

echo ""

if [[ $# -lt 2 ]]; then 
	echoerrorflash "Oh, computer says no! Number of arguments found $#."
	script_arguments_error "You must supply correct (number of) arguments when running *** rename.files ***!"

else

	if ! [ -f "$1" ];then
		echoerrorflash "No valid recode file found."
		echoerrorflash "Usage "$(basename "$0")" recodefile.txt /input/dir/"
		exit 1
	fi
	if ! [ -d "$2" ];then
		echoerrorflash "No valid directory found."
		echoerrorflash "Usage "$(basename "$0")" recodefile.txt /input/dir/"
		exit 1
	fi
	
	echo ""
	echo "------------------------------------------------------------------------------------"
	echobold "Input was correct. Preparing move."
	while IFS='' read -r FILENAMES || [[ -n "$FILENAMES" ]]; do
		LINE=${FILENAMES}
	
		OLDNAME=$(echo "${LINE}" | awk 'BEGIN{FS="\t"} {print $1}' )
		NEWNAME=$(echo "${LINE}" | awk 'BEGIN{FS="\t"} {print $2}' )
		echo ""
		echo "The old filename is: [ $(ls "${OLDNAME}") ]"
		echo "The new filename is: [ $NEWNAME ]"

		if [ ! -z "${OLDNAME}" ]; then # if non-zero
		echoerrorflash "The old filename is not present. "
	
			if [ ! -z "$NEWNAME" ]; then # if non-zero
		
			echo  "Moving files..."
			mv -nv "$2/${OLDNAME}"  "$2/$NEWNAME" # move the old name to the new (second) name"

			fi
		fi
	done < "$1"

### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message

echo ""
echobold "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "Wow. I'm all done buddy. What a job! let's have 🍻  and 🖖 !"
date

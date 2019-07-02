#!/bin/bash

### Creating display functions
### Setting colouring
NONE='\033[00m'
BOLD='\033[1m'
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

function echocyan { #'echobold' is the function name
    echo -e "${CYAN}${1}${NONE}" # this is whatever the function needs to execute.
}
function echobold { #'echobold' is the function name
    echo -e "${BOLD}${1}${NONE}" # this is whatever the function needs to execute, note ${1} is the text for echo
}
function echoitalic { #'echobold' is the function name
    echo -e "\033[3m${1}\033[0m" # this is whatever the function needs to execute.
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                             DIRECTORY CREATOR"
echo ""
echoitalic "* Written by  : Tim G.M. van de Kerkhof; Sander W. van der Laan"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2019-07-02"
echoitalic "* Version     : 1.0.2"
echo ""
echoitalic "* Description : This script will create directories using slideDirectory from "
echoitalic "                slideToolKit."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo ""
echocyan "Fix filenames and replace 'spaces' with '_'."
for f in *\ *; do 
	mv -v "$f" "${f// /_}"
done

echo ""
echocyan "Creating directories for NDPI-files."
# old version macOS based, '-iname' goes iteratively through all the folders in the folder
# find "$(pwd)" -iname "*.ndpi" -exec /hpc/local/CentOS7/dhl_ec/software/slideToolKit/slideDirectory -f "{}" \;
find  *.ndpi -exec $(command -v slideDirectory) -f "{}" \;

echo ""
echocyan "Creating directories for TIF-files."
# old version macOS based, '-iname' goes iteratively through all the folders in the folder
# find "$(pwd)" -iname "*.TIF" -exec /hpc/local/CentOS7/dhl_ec/software/slideToolKit/slideDirectory -f "{}" \;
find  *.TIF -exec $(command -v slideDirectory) -f "{}" \;

echo ""
echocyan "Creating directories for tif-files."
# old version macOS based, '-iname' goes iteratively through all the folders in the folder
# find "$(pwd)" -iname "*.TIF" -exec /hpc/local/CentOS7/dhl_ec/software/slideToolKit/slideDirectory -f "{}" \;
find  *.tif -exec $(command -v slideDirectory) -f "{}" \;

echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "Wow. I'm all done buddy. What a job! let's have a beer!"
date

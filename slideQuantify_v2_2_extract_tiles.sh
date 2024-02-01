#!/bin/bash
#
# Description: Runs slideTiles to normalize images as part of a slideQuantify job-session.
# 
# The MIT License (MIT)
# Copyright (c) 2024, Tim Peters 
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
	echo "+ Copyright (c) 2024-${THISYEAR} Tim Peters                                                      +"
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
	echoerror ""
	echoerror "- Argument #1  -- project_dir. Path to project directory. Should contain _ndpi and/or _tif folders."
	echoerror "- Argument #2  -- masks_dir. Path to directory containing the masks for the images."
	echoerror "- Argument #3  -- layer. Which magnification layer of the image should be taken."
	echoerror "- Argument #4  -- tile_size. Size of the extracted tiles."
	echoerror "- Argument #5  -- study_number. Study number of the processed image"
	echoerror ""
	echoerror "An example command would be: slideQuantify_2_extract_tiles.sh [--arg1= /path/to/dir] [--arg2= /path/to/dir] [--arg3= 1] [--arg4= 200-] [--arg5= AE21]"
	echoerror ""
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	# The wrong arguments are passed, so we'll exit the script now!
	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                          slideQuantify: Tiling"
echo ""
echoitalic "* Written by  : Tim Peters"
echoitalic "* E-mail      : t.s.peters-4@umcutrecht.nl"
echoitalic "* Last update : 2024-01-09"
echoitalic "* Version     : 1.0.0"
echo ""
echoitalic "* Description : This script will create tiles from a given image for the "
echoitalic "                slideToolKit analyses."
echoitalic "                This is SLURM based."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

echo ""

# loading required modules 
### Loading the CellProfiler-Anaconda3.8 environment
### You need to also have the conda init lines in your .bash_profile/.bashrc file
echo "..... > loading required anaconda environment containing the CellProfiler installation..."
module load mambaforge3
eval "$(conda shell.bash hook)"
conda activate cp4
echo Loaded conda environment: $CONDA_PREFIX
echo ""

### Set slideToolKit DIRECTORY
SLIDETOOLKITDIR="/hpc/local/Rocky8/dhl_ec/software/slideToolKit"

OUT_DIR="${1}/slideToolkit/_tiles"
DATA_DIR="${1}"
MASK_DIR="${2}"
LAYER="${3}"
TILESIZE="${4}"

SAVE_DIR=$OUT_DIR"_layer"$LAYER

NR="${5}"

echo "..... > Given script parameters..."
echo OUT_DIR= $OUT_DIR
echo DATA_DIR= $DATA_DIR
echo MASK_DIR= $MASK_DIR
echo LAYER= $LAYER
echo TILESIZE= $TILESIZE
echo SAVE_DIR= $SAVE_DIR
echo NR= $NR
echo ""

if [ -d $SAVE_DIR/$NR.*/ ];
then
	echo "$NR already has extracted tiles"
else
	if [ -f $DATA_DIR/_ndpi/$NR.*.ndpi ]; then
    	echo "NDPI of $NR found."
		python3 $SLIDETOOLKITDIR/slideExtractTiles.py --layer $LAYER --tile_size $TILESIZE --file $DATA_DIR/_ndpi/$NR.*.ndpi --mask $MASK_DIR/_ndpi/$NR.*.jpg --out $SAVE_DIR/
	elif [ -f $DATA_DIR/_tif/$NR.*.TIF ]; then
		echo "TIF of $NR found."
		python3 $SLIDETOOLKITDIR/slideExtractTiles.py --layer $LAYER --tile_size $TILESIZE --file $DATA_DIR/_tif/$NR.*.TIF --mask $MASK_DIR/_tif/$NR.*.jpg --out $SAVE_DIR/
	elif [ -f $DATA_DIR/_images_dropzone/$NR.*.ndpi ]; then
		echo "[CUSTOM (_images_dropzone)] NDPI of $NR found."
		python3 $SLIDETOOLKITDIR/slideExtractTiles.py --layer $LAYER --tile_size $TILESIZE --file $DATA_DIR/_images_dropzone/$NR.*.ndpi --mask $MASK_DIR/CD68/$NR.*.jpg --out $SAVE_DIR/
	elif [ -f $DATA_DIR/_images_dropzone/$NR.*.TIF ]; then
		echo "[CUSTOM (_images_dropzone)] TIF of $NR found."
		python3 $SLIDETOOLKITDIR/slideExtractTiles.py --layer $LAYER --tile_size $TILESIZE --file $DATA_DIR/_images_dropzone/$NR.*.TIF --mask $MASK_DIR/CD68/$NR.*.jpg --out $SAVE_DIR/
	else
		echo "No NDPI or TIF of $NR found."
	fi
fi

script_copyright_message

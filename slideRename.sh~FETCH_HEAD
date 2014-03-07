#!/bin/bash
#
# Description: Rename virtual slide using thumbnail
# Copyright (C) 2014, B.G.L. Nelissen. All rights reserved.
#
################################################################################
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
#   Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# 
#   Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
################################################################################
# Respect the Google Shell style guide.
# http://google-styleguide.googlecode.com/svn/trunk/shell.xml

# Variables
SCRIPTNAME=$(basename $0)
DESCRIPTIONSHORT="Rename virtual slide using thumbnail"
DEPENDENCIES=("display") # imageMagick needs to be compiled with x11 support for OSX
DEFAULTLAYER=0 # 0 = thumbnail

# Errors go to stderr
err() {
  echo "ERROR: $@" >&2
}

# usage message
usage() {
cat <<- EOF
usage:  $SCRIPTNAME [options] [path/]file
        [--help]
EOF
}

# help message
helpMessage() {
cat <<- EOF
${SCRIPTNAME}: ${DESCRIPTIONSHORT}

$(usage)

options:
  -f, --file[=FILE]         virtual slide to create mask from

  --help                    display this help and exit

examples:
  $SCRIPTNAME file.tif
  $SCRIPTNAME  --file="file.tif"

multiple files at once:
  find -L ./  -name '*.tif' -exec $SCRIPTNAME {}

dependencies: $DEPENDENCIES

Type in the name and press [enter] to rename the file. You can use a
regular barcode scanner.

Report bugs to <b.g.l.nelissen@gmail.com>
slideToolkit (C) 2014, B.G.L. Nelissen
EOF
}

# MENU
# Empty variables
FILE=""
# illegal option
illegalOption() {
cat <<- EOF
$SCRIPTNAME: illegal option $1
$(usage)
EOF
exit 1
}
# loop through options
while :
do
  case $1 in
    --help | -\?)
      helpMessage
      exit 0 ;;
    -f | --file)
      FILE=$2
      shift 2 ;;
    --file=*)
      FILE=${1#*=}
      shift ;;
    --) # End of all options
      shift
      break ;;
    -*)
      illegalOption "$1"
      shift ;;
    *)  # no more options. Stop while loop
      break ;;
  esac
done
# DEFAULTS
# set FILE
if [ "$FILE" != "" ]; then
  FILE="$FILE"
else
  FILE="$1"
fi

# requirements
checkRequirements() {
  if ! [[ -f "$FILE" ]] ; then
    err "No such file: $FILE"
    usage
    exit 1
  fi
}

# Dependencies
checkDependencies(){
  DEPENDENCIES="$DEPENDENCIES"
  DEPS=""
  for DEP in $DEPENDENCIES; do
    if [[ 0 != $(command -v "$DEP" >/dev/null ;echo $?) ]]; then
      DEPS=$(echo "$DEPS \"$DEP\"") # create `array` with unknown dependencies
    fi
  done
  if [[ "" != $(echo "$DEPS" | perl -p -e 's/ //g') ]]; then
    for d in $DEPS; do
      echo "Missing dependency: \"$d\""
    done
    exit 1
  fi
}

# actual program
programOutput(){
  # set variables
  FILE="$FILE"
  # path variables
	LAYER="$LAYER"
  FILEFULL="$(echo $(cd $(dirname $FILE); pwd)/$(basename $FILE))" # full path $FULL
  BASENAME=$(basename "$FILEFULL")    # basename
	DIRNAME=$(dirname "$FILE")          # dirname
  EXTENSION="${BASENAME##*.}"         # extension
  FILEPATH="${FILEFULL%.*}"           # full path, no extension
  FILENAME="${BASENAME%.*}"           # filename, no extension"
	
	# let's roll
#	clear

	# kill all running preview windows
	# kill $(ps -ax | grep -i [p]review | awk '{print $1}') > /dev/null 2>&1

    #   show file to rename using osx open
	# display -a App -g stay in background "${FILE}"
# 	open -a Preview -g "$FILE" &
# 	if [ $? -ne 0 ]; then
# 	    err "Can not start Preview app."
# 	    exit 1
# 	fi
	# start x11
	open -a XQuartz
  osascript -e 'tell application "Terminal" to activate'
	
	# show image
  display "$FILE[0]" &
	
  osascript -e 'tell application "Terminal" to activate'
  #   ask for a named
  echo "Keep this window in focus (quit: ctrl c)"
  echo "Scan/Type barcode... [ AE1234.STAIN enter ]"
  read NEWNAME
  NEWNAME="$(echo $NEWNAME | sed 's/^.*\(AE.*\)/\1/g')" # remove invisible characters [bug?]
  #   rename the file
  if [ -n "$NEWNAME" ]; then
      # Move files
      echo "$FILE" "${DIRNAME}/${NEWNAME}.${EXTENSION}"
  else
      echo "No new filename given."
      echo "exit 1"
      exit 1
  fi
  sleep 1
}

# all check?
checkRequirements
checkDependencies 

# lets go!
# actual program
programOutput
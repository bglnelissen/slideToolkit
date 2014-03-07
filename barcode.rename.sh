#!/bin/bash
# b.nelissen
# rename files by barcode or other
# depends on imagemagick (display function)

# for each tif file
#   show file to rename
#   ask for a named
#   rename the file
#   go to next file
# done

if [ -f "$1" ]; then
	# set variables
	FILE="$1"
	DIRNAME=$(dirname "$FILE")
	BASENAME=$(basename "$FILE") # BASENAME
	EXTENSION="${BASENAME##*.}"
	FILENAME="${FILE%.*}" # full path without EXTENSION
	
	# let's roll
	clear
	echo "$BASENAME"
	
	# skip if file is not a thumbnail
	if [ 0 == $(echo $BASENAME | grep -c thumb.png$ ) ];then
	    echo "filename does not end with \"thumb.png\""
	    echo "skip this file"
	    exit 1
	fi

	# kill all running preview windows
	kill $(ps -ax | grep -i [p]review | awk '{print $1}') > /dev/null 2>&1

    #   show file to rename using osx open
	# display -a App -g stay in background "${FILE}"
	open -a Preview -g "${FILE}"
	if [ $? -ne 0 ]; then
	    echo "Error starting Preview app."
	    exit 1
	fi
	
    #   ask for a named
    echo "Keep this window in focus (quit: ctrl c)"
    echo "Scan/Type barcode... [ AE1234.STAIN enter ]"
	read -s NEWNAME
	NEWNAME=$(echo $NEWNAME | sed 's/^.*\(AE.*\)/\1/g') # remove invisible characters [bug?]
	#   rename the file
    if [ -n "$NEWNAME" ]; then
        # Move files
        mv -v ${FILE} ${DIRNAME}/${NEWNAME}.${EXTENSION}
    else
        echo "No new filename given."
        echo "exit 1"
        exit 1
    fi
else
	echo "NO FILE: $FILE"
fi

# kill all running preview windows
kill $(ps -ax | grep -i [p]review | awk '{print $1}') > /dev/null 2>&1
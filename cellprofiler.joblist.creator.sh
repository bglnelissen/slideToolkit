#!/bin/bash
# create joblist with multiple pipelines
# for i in $(find ./Slides -name *.tif); do cellprofiler.joblist.creator.sh $i pipeline.cp joblist.sh; done
# b.nelissen

# Variables
CPBIN="/hpc/local/CentOS6/dhl_ec/software/CellProfiler-2.1-beta/bin/cellprofiler"

# create absolute 'real' paths
absolutepath () {
    p="$(echo $(cd $(dirname $1); pwd)/$(basename $1))"
    echo "$p"
}

# create multiple pipelines for each folder
# expect the original .tif files as orientation
if [[ -f "$1" && -f "$2" && "${1##*.}"=='tif' ]]; then
    # set variables
    FILE=$(absolutepath "$1")
    PIPELINE=$(absolutepath "$2")
    FILENAMEEXT=$(basename "$FILE")
    EXTENSION="${FILENAMEEXT##*.}"
    FILENAME="${FILE%.*}" # full path without extension
    NAME="${FILENAMEEXT%.*}" # filename only without extension
    IMAGEDIR="${FILENAME}"
    OUTPUTDIR="${FILENAME}.output"
    mkdir -p "$OUTPUTDIR" # outputdir must exist
    
    # create job for qsub
    JOB="qsub -N \"${NAME}.cp\" -pe threaded 3 -q short -e \"${FILENAME}.cellprofiler.e.txt\" -o \"${FILENAME}.cellprofiler.o.txt\" $CPBIN -r -c -i $IMAGEDIR -o $OUTPUTDIR -p $PIPELINE" 
    echo "$JOB"
    
    # write output to file if a file is set
    if [ ! -z "$3" ]; then    
        # touch and mod
        touch "${3}"
        chmod 755 "${3}"
        echo "$JOB" >> "$3"
    fi
else
    echo
    echo "Usage:"
    echo "    $(basename "$0") path.to.slide.tif path.to.pipeline.cp joblist.sh"
    echo
    echo "Use pathnames without spaces"
	echo "Set variables:"
    echo "    Input tif: \"$1\" [This .tif file is used as a location reference]"
    echo "    Pipeline:  \"$2\" [This pipeline will be used for the input .tif file]"
    echo "    Joblist:   \"$3\" [The job will be saved in this list, optional]"
    echo
    echo "Pro tip; run this script in a loop:"
    echo '    for i in $(find -L ./Slides -name *.tif); do cellprofiler.joblist.creator.sh $i pipeline.cp joblist.sh; done'
    exit 1
fi

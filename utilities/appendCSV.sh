#!/bin/bash
#
#$ -S /bin/bash 																		# the type of BASH you'd like to use
#$ -N Appender."$1" 																		# the name of this script
# -hold_jid some_other_basic_bash_script  												# the current script (basic_bash_script) will hold until some_other_basic_bash_script has finished
#$ -o /hpc/dhl_ec/VirtualSlides/Appender."$1".log  											# the log file of this job
#$ -e /hpc/dhl_ec/VirtualSlides/Appender."$1".errors 										# the error file of this job
#$ -l h_rt=00:30:00  																	# h_rt=[max time, e.g. 02:02:01] - this is the time you think the script will take
#$ -l h_vmem=4G  																		#  h_vmem=[max. mem, e.g. 45G] - this is the amount of memory you think your script will use
# -l tmpspace=64G  																		# this is the amount of temporary space you think your script will use
#$ -M s.w.vanderlaan-2@umcutrecht.nl  													# you can send yourself emails when the job is done; "-M" and "-m" go hand in hand
#$ -m ea  																				# you can choose: b=begin of job; e=end of job; a=abort of job; s=suspended job; n=no mail is send
#$ -cwd  																				# set the job start to the current directory - so all the things in this script are relative to the current directory!!!
#
### INTERACTIVE SHELLS
# You can also schedule an interactive shell, e.g.:
#
# qlogin -N "basic_bash_script" -l h_rt=02:00:00 -l h_vmem=24G -M s.w.vanderlaan-2@umcutrecht.nl -m ea
#
# You can use the variables above (indicated by "#$") to set some things for the submission system.
# Another useful tip: you can set a job to run after another has finished. Name the job 
# with "-N SOMENAME" and hold the other job with -hold_jid SOMENAME". 
# Further instructions: https://wiki.bioinformatics.umcutrecht.nl/bin/view/HPC/HowToS#Run_a_job_after_your_other_jobs
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
	echoerror "- Argument #1  -- name of the stain as it appears in the filenames, e.g. FIBRIN."
	echoerror "- Argument #2  -- study type of the analysis, e.g. AE or AAA."
	echoerror "- Argument #3  -- image file type, e.g. TIF, NDPI."
	echoerror "- Argument #4  -- (the path to) the filename, e.g. Image.csv.gz, the script will automatically append STAIN, e.g. STAIN_Image.csv.gz"
	echoerror ""
	echoerror "An example command would be: appendCSV [arg1: STAIN] [arg2: STUDYTYPE ] [arg3: IMAGETYPE ] [arg4: Output_Image.csv.gz] "
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  	# The wrong arguments are passed, so we'll exit the script now!
  	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                              RESULT APPENDER"
echo ""
echoitalic "* Written by  : Tim G.M. van de Kerkhof; Sander W. van der Laan"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2019-07-15"
echoitalic "* Version     : v1.0.1"
echo ""
echoitalic "* Description : This script will collect results and append these in a CSV."
echoitalic "                Input CSV-files are expected to be gzipped."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "Today's: "$(date)
TODAY=$(date +"%Y%m%d") # set Today

echo ""
### REQUIRED | GENERALS	
STAIN="$1" # Depends on arg1
STUDYTYPE="$2"
IMAGETYPE="$3"
RESULTSFILENAME="$4"

if [[ $# -lt 4 ]]; then 
	echoerrorflash "Oh, computer says no! Number of arguments found "$#"."
	script_arguments_error "You must supply correct (number of) arguments when running *** appendCSV ***!"

else

	OutFileName="${TODAY}.${STAIN}.${STUDYTYPE}.${IMAGETYPE}.ImageExp.csv" # Fix the output name
	
	echo ""
	echoitalic "Creating a new log."
	# make a new append.log
	rm -v *append.log
	echo "STUDYNUMBER FILENAME" > ${TODAY}.${STAIN}.${STUDYTYPE}.${IMAGETYPE}.append.log
	
	i=0 # Reset a counter
	echo ""
	echoitalic "Collecting data for:"
	for filename in ${STUDYTYPE}*/cp_output/${STAIN}_${RESULTSFILENAME}; do 
		if [ "$filename"  != "$OutFileName" ] ; then # Avoid recursion
		
			cols=$(zcat "$filename" | awk -F, '{ print NF }' | uniq | wc -l)
			if [[ "$cols" -gt 1 ]]; then
				STUDYNUMBER=${filename%%\/*} # Remove everything from the first slash >> https://unix.stackexchange.com/questions/268134/extract-a-specific-part-of-the-path-of-a-file
				echo "**ERROR** no new line for end-of-file for [ $STUDYNUMBER ]."
				echo "$STUDYNUMBER $filename" >> ${TODAY}.${STAIN}.${STUDYTYPE}.${IMAGETYPE}.append.log
		
			else	
				if [[ $i -eq 0 ]] ;  then
					### DEBUG
					### echo "DEBUG: check head first file"
					### zcat "$filename" | head -1
					zcat "$filename" | head -1 > "$OutFileName" # Copy header if it is the first file
				else
					echoitalic " ... [ ${filename} ] ..."
					### DEBUG
					### echo "DEBUG: check head next file"
					### zcat "$filename" | head -2
					zcat "$filename" | tail -n +2 >> "$OutFileName" # Append from the 2nd line each file
					
					### DEBUG
					### ls -lh "$OutFileName"
				fi
			fi
		fi
		i=$(( $i + 1 )) # Increase the counter
	done

	echo ""
	echoitalic "Gzipping the shizzle."
	gzip -vf ${TODAY}.${STAIN}.${STUDYTYPE}.${IMAGETYPE}.ImageExp.csv

	echo ""
	echoitalic "Checking the log -- note: no results is a good thing."
	cat ${TODAY}.${STAIN}.${STUDYTYPE}.${IMAGETYPE}.append.log
	
	echo ""

### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message

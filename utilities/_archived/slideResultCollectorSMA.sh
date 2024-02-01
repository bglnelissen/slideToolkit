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
	echo "+ Copyright (c) 2015-${THISYEAR} Sander W. van der Laan                                                        +"
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
	echoerror "- Argument #1  indicates the stain used."
	echoerror ""
	echoerror "An example command would be: slideResultCollectorSMA.sh [arg1: STAIN] "
	echoerror "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
  	# The wrong arguments are passed, so we'll exit the script now!
  	exit 1
}

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echobold "                         slideResultCollector for SMA"
echo ""
echoitalic "* Written by  : Sander W. van der Laan"
echoitalic "* E-mail      : s.w.vanderlaan-2@umcutrecht.nl"
echoitalic "* Last update : 2019-01-23"
echoitalic "* Version     : 1.0.1"
echo ""
echoitalic "* Description : This script will collect data for a object quantification,"
echoitalic "                such as DAB based SMA."
echo ""
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

# filename: SMA_DAB_object.txt
# ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number
# 
# filename: SMA_nuclei_DAB.txt
# ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number
# 
# filename: SMA_HE_object.txt
# ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number
# 
# filename: SMA_nuclei_HE.txt
# ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number
# 
# filename: SMA_Image.txt
# AreaOccupied_AreaOccupied_DAB_object_yellow	AreaOccupied_AreaOccupied_HE_object_green	AreaOccupied_AreaOccupied_nuclei_DAB_red	AreaOccupied_AreaOccupied_nuclei_HE_blue	AreaOccupied_Perimeter_DAB_object_yellow	AreaOccupied_Perimeter_HE_object_green	AreaOccupied_Perimeter_nuclei_DAB_red	AreaOccupied_Perimeter_nuclei_HE_blue	AreaOccupied_TotalArea_DAB_object_yellow	AreaOccupied_TotalArea_HE_object_green	AreaOccupied_TotalArea_nuclei_DAB_red	AreaOccupied_TotalArea_nuclei_HE_blue	Channel_EntropyImage	Channel_Original	Count_DAB_object	Count_HE_object	Count_nuclei_DAB	Count_nuclei_HE	ExecutionTime_01Images	ExecutionTime_02Metadata	ExecutionTime_03NamesAndTypes	ExecutionTime_04Groups	ExecutionTime_05ColorToGray	ExecutionTime_06Morph	ExecutionTime_07UnmixColors	ExecutionTime_08IdentifyPrimaryObjects	ExecutionTime_09IdentifyPrimaryObjects	ExecutionTime_10MaskImage	ExecutionTime_11MaskImage	ExecutionTime_12IdentifyPrimaryObjects	ExecutionTime_13IdentifyPrimaryObjects	ExecutionTime_14OverlayOutlines	ExecutionTime_15SaveImages	ExecutionTime_16MeasureImageAreaOccupied	FileName_EntropyImage	FileName_Original	Frame_EntropyImage	Frame_Original	Group_Index	Group_Number	Height_EntropyImage	Height_Original	ImageNumber	ImageSet_ImageSet	MD5Digest_EntropyImage	MD5Digest_Original	Metadata_FileLocation	Metadata_Frame	Metadata_NR	Metadata_STAIN	Metadata_Series	Metadata_X	Metadata_Y	ModuleError_01Images	ModuleError_02Metadata	ModuleError_03NamesAndTypes	ModuleError_04Groups	ModuleError_05ColorToGray	ModuleError_06Morph	ModuleError_07UnmixColors	ModuleError_08IdentifyPrimaryObjects	ModuleError_09IdentifyPrimaryObjects	ModuleError_10MaskImage	ModuleError_11MaskImage	ModuleError_12IdentifyPrimaryObjects	ModuleError_13IdentifyPrimaryObjects	ModuleError_14OverlayOutlines	ModuleError_15SaveImages	ModuleError_16MeasureImageAreaOccupied	PathName_EntropyImage	PathName_Original	Scaling_EntropyImage	Scaling_Original	Series_EntropyImage	Series_Original	Threshold_FinalThreshold_DAB_object	Threshold_FinalThreshold_HE_object	Threshold_FinalThreshold_nuclei_DAB	Threshold_FinalThreshold_nuclei_HE	Threshold_OrigThreshold_DAB_object	Threshold_OrigThreshold_HE_object	Threshold_OrigThreshold_nuclei_DAB	Threshold_OrigThreshold_nuclei_HE	Threshold_SumOfEntropies_DAB_object	Threshold_SumOfEntropies_HE_object	Threshold_SumOfEntropies_nuclei_DAB	Threshold_SumOfEntropies_nuclei_HE	Threshold_WeightedVariance_DAB_object	Threshold_WeightedVariance_HE_object	Threshold_WeightedVariance_nuclei_DAB	Threshold_WeightedVariance_nuclei_HE	URL_EntropyImage	URL_Original	Width_EntropyImage	Width_Original
#
# filename: SMA_Experiment.txt
# Key	Value


### REQUIRED | GENERALS	
STAIN="$1" # Depends on arg1 

### START of if-else statement for the number of command-line arguments passed ###
if [[ $# -lt 1 ]]; then 
	echo "Oh, computer says no! Number of arguments found "$#"."
	script_arguments_error "You must supply correct arguments when running a *** RESULT CONCATENATOR ***!"
		
else
	
	echo "All arguments are passed and correct. We will collect data for stain: [ $STAIN ] ."

	echo ""
	echocyan "Collecting data for DAB OBJECTS."
# 	filename: SMA_DAB_object.txt
# 	ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number

	echo "ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number" > ${STAIN}_DAB_OBJECT.results.txt

	for AE_NUM in $(ls -d AE*); do 
		echo "* checking data from $AE_NUM ..."
		cat $AE_NUM/cp_output/${STAIN}_DAB_object.txt | tail -n +2 >> ${STAIN}_DAB_OBJECT.results.txt
		gzip -vf $AE_NUM/cp_output/${STAIN}_DAB_object.txt
	done
	
	echo ""
	echo "Let's get a-head:" 
	head ${STAIN}_DAB_OBJECT.results.txt 
	
	echo ""
	echo "Let's tail that shizzle:" 
	tail ${STAIN}_DAB_OBJECT.results.txt 

	echo ""
	echo "Let's get a count of lines:" 
	cat ${STAIN}_DAB_OBJECT.results.txt | tail -n +2 | wc -l

	echo ""
	echo "Saving space by gzipping that shizzle ..."
	gzip -vf ${STAIN}_DAB_OBJECT.results.txt

	echo ""
	echocyan "Collecting data for DAB NUCLEI."
	# filename: SMA_nuclei_DAB.txt
	# ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number

	echo "ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number" > ${STAIN}_NUCLEI_DAB.results.txt

	for AE_NUM in $(ls -d AE*); do 
		echo "* checking data from $AE_NUM ..."
		cat $AE_NUM/cp_output/${STAIN}_nuclei_DAB.txt | tail -n +2 >> ${STAIN}_NUCLEI_DAB.results.txt
		gzip -vf $AE_NUM/cp_output/${STAIN}_nuclei_DAB.txt
	done

	echo ""
	echo "Let's get a-head:" 
	head ${STAIN}_NUCLEI_DAB.results.txt 
	
	echo ""
	echo "Let's tail that shizzle:" 
	tail ${STAIN}_NUCLEI_DAB.results.txt 

	echo ""
	echo "Let's get a count of lines:" 
	cat ${STAIN}_NUCLEI_DAB.results.txt | tail -n +2 | wc -l
	
	echo ""
	echo "Saving space by gzipping that shizzle ..."
	gzip -vf ${STAIN}_NUCLEI_DAB.results.txt
	
	echo ""
	echocyan "Collecting data for HE OBJECTS."
	# 	filename: SMA_HE_object.txt
	# 	ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number

	echo "ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number" > ${STAIN}_HE_OBJECT.results.txt

	for AE_NUM in $(ls -d AE*); do 
		echo "* checking data from $AE_NUM ..."
		cat $AE_NUM/cp_output/${STAIN}_HE_object.txt | tail -n +2 >> ${STAIN}_HE_OBJECT.results.txt
		gzip -vf $AE_NUM/cp_output/${STAIN}_HE_object.txt
	done
	
	echo ""
	echo "Let's get a-head:" 
	head ${STAIN}_HE_OBJECT.results.txt 
	
	echo ""
	echo "Let's tail that shizzle:" 
	tail ${STAIN}_HE_OBJECT.results.txt 

	echo ""
	echo "Let's get a count of lines:" 
	cat ${STAIN}_HE_OBJECT.results.txt | tail -n +2 | wc -l

	echo ""
	echo "Saving space by gzipping that shizzle ..."
	gzip -vf ${STAIN}_HE_OBJECT.results.txt
	
	echo ""
	echocyan "Collecting data for HE NUCLEI."
	# filename: SMA_nuclei_HE.txt
	# ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number

	echo "ImageNumber	ObjectNumber	Location_Center_X	Location_Center_Y	Number_Object_Number" > ${STAIN}_NUCLEI_HE.results.txt

	for AE_NUM in $(ls -d AE*); do 
		echo "* checking data from $AE_NUM ..."
		cat $AE_NUM/cp_output/${STAIN}_nuclei_HE.txt | tail -n +2 >> ${STAIN}_NUCLEI_HE.results.txt
		gzip -fv $AE_NUM/cp_output/${STAIN}_nuclei_HE.txt
	done

	echo ""
	echo "Let's get a-head:" 
	head ${STAIN}_NUCLEI_HE.results.txt 
	
	echo ""
	echo "Let's tail that shizzle:" 
	tail ${STAIN}_NUCLEI_HE.results.txt 

	echo ""
	echo "Let's get a count of lines:" 
	cat ${STAIN}_NUCLEI_HE.results.txt | tail -n +2 | wc -l
	
	echo ""
	echo "Saving space by gzipping that shizzle ..."
	gzip -fv ${STAIN}_NUCLEI_HE.results.txt

	echo ""
	echocyan "Collecting data for IMAGE."
	# filename: SMA_Image.txt
	# AreaOccupied_AreaOccupied_DAB_object_yellow	AreaOccupied_AreaOccupied_HE_object_green	AreaOccupied_AreaOccupied_nuclei_DAB_red	AreaOccupied_AreaOccupied_nuclei_HE_blue	AreaOccupied_Perimeter_DAB_object_yellow	AreaOccupied_Perimeter_HE_object_green	AreaOccupied_Perimeter_nuclei_DAB_red	AreaOccupied_Perimeter_nuclei_HE_blue	AreaOccupied_TotalArea_DAB_object_yellow	AreaOccupied_TotalArea_HE_object_green	AreaOccupied_TotalArea_nuclei_DAB_red	AreaOccupied_TotalArea_nuclei_HE_blue	Channel_EntropyImage	Channel_Original	Count_DAB_object	Count_HE_object	Count_nuclei_DAB	Count_nuclei_HE	ExecutionTime_01Images	ExecutionTime_02Metadata	ExecutionTime_03NamesAndTypes	ExecutionTime_04Groups	ExecutionTime_05ColorToGray	ExecutionTime_06Morph	ExecutionTime_07UnmixColors	ExecutionTime_08IdentifyPrimaryObjects	ExecutionTime_09IdentifyPrimaryObjects	ExecutionTime_10MaskImage	ExecutionTime_11MaskImage	ExecutionTime_12IdentifyPrimaryObjects	ExecutionTime_13IdentifyPrimaryObjects	ExecutionTime_14OverlayOutlines	ExecutionTime_15SaveImages	ExecutionTime_16MeasureImageAreaOccupied	FileName_EntropyImage	FileName_Original	Frame_EntropyImage	Frame_Original	Group_Index	Group_Number	Height_EntropyImage	Height_Original	ImageNumber	ImageSet_ImageSet	MD5Digest_EntropyImage	MD5Digest_Original	Metadata_FileLocation	Metadata_Frame	Metadata_NR	Metadata_STAIN	Metadata_Series	Metadata_X	Metadata_Y	ModuleError_01Images	ModuleError_02Metadata	ModuleError_03NamesAndTypes	ModuleError_04Groups	ModuleError_05ColorToGray	ModuleError_06Morph	ModuleError_07UnmixColors	ModuleError_08IdentifyPrimaryObjects	ModuleError_09IdentifyPrimaryObjects	ModuleError_10MaskImage	ModuleError_11MaskImage	ModuleError_12IdentifyPrimaryObjects	ModuleError_13IdentifyPrimaryObjects	ModuleError_14OverlayOutlines	ModuleError_15SaveImages	ModuleError_16MeasureImageAreaOccupied	PathName_EntropyImage	PathName_Original	Scaling_EntropyImage	Scaling_Original	Series_EntropyImage	Series_Original	Threshold_FinalThreshold_DAB_object	Threshold_FinalThreshold_HE_object	Threshold_FinalThreshold_nuclei_DAB	Threshold_FinalThreshold_nuclei_HE	Threshold_OrigThreshold_DAB_object	Threshold_OrigThreshold_HE_object	Threshold_OrigThreshold_nuclei_DAB	Threshold_OrigThreshold_nuclei_HE	Threshold_SumOfEntropies_DAB_object	Threshold_SumOfEntropies_HE_object	Threshold_SumOfEntropies_nuclei_DAB	Threshold_SumOfEntropies_nuclei_HE	Threshold_WeightedVariance_DAB_object	Threshold_WeightedVariance_HE_object	Threshold_WeightedVariance_nuclei_DAB	Threshold_WeightedVariance_nuclei_HE	URL_EntropyImage	URL_Original	Width_EntropyImage	Width_Original

	echo "AreaOccupied_AreaOccupied_DAB_object_yellow	AreaOccupied_AreaOccupied_HE_object_green	AreaOccupied_AreaOccupied_nuclei_DAB_red	AreaOccupied_AreaOccupied_nuclei_HE_blue	AreaOccupied_Perimeter_DAB_object_yellow	AreaOccupied_Perimeter_HE_object_green	AreaOccupied_Perimeter_nuclei_DAB_red	AreaOccupied_Perimeter_nuclei_HE_blue	AreaOccupied_TotalArea_DAB_object_yellow	AreaOccupied_TotalArea_HE_object_green	AreaOccupied_TotalArea_nuclei_DAB_red	AreaOccupied_TotalArea_nuclei_HE_blue	Channel_EntropyImage	Channel_Original	Count_DAB_object	Count_HE_object	Count_nuclei_DAB	Count_nuclei_HE	ExecutionTime_01Images	ExecutionTime_02Metadata	ExecutionTime_03NamesAndTypes	ExecutionTime_04Groups	ExecutionTime_05ColorToGray	ExecutionTime_06Morph	ExecutionTime_07UnmixColors	ExecutionTime_08IdentifyPrimaryObjects	ExecutionTime_09IdentifyPrimaryObjects	ExecutionTime_10MaskImage	ExecutionTime_11MaskImage	ExecutionTime_12IdentifyPrimaryObjects	ExecutionTime_13IdentifyPrimaryObjects	ExecutionTime_14OverlayOutlines	ExecutionTime_15SaveImages	ExecutionTime_16MeasureImageAreaOccupied	FileName_EntropyImage	FileName_Original	Frame_EntropyImage	Frame_Original	Group_Index	Group_Number	Height_EntropyImage	Height_Original	ImageNumber	ImageSet_ImageSet	MD5Digest_EntropyImage	MD5Digest_Original	Metadata_FileLocation	Metadata_Frame	Metadata_NR	Metadata_STAIN	Metadata_Series	Metadata_X	Metadata_Y	ModuleError_01Images	ModuleError_02Metadata	ModuleError_03NamesAndTypes	ModuleError_04Groups	ModuleError_05ColorToGray	ModuleError_06Morph	ModuleError_07UnmixColors	ModuleError_08IdentifyPrimaryObjects	ModuleError_09IdentifyPrimaryObjects	ModuleError_10MaskImage	ModuleError_11MaskImage	ModuleError_12IdentifyPrimaryObjects	ModuleError_13IdentifyPrimaryObjects	ModuleError_14OverlayOutlines	ModuleError_15SaveImages	ModuleError_16MeasureImageAreaOccupied	PathName_EntropyImage	PathName_Original	Scaling_EntropyImage	Scaling_Original	Series_EntropyImage	Series_Original	Threshold_FinalThreshold_DAB_object	Threshold_FinalThreshold_HE_object	Threshold_FinalThreshold_nuclei_DAB	Threshold_FinalThreshold_nuclei_HE	Threshold_OrigThreshold_DAB_object	Threshold_OrigThreshold_HE_object	Threshold_OrigThreshold_nuclei_DAB	Threshold_OrigThreshold_nuclei_HE	Threshold_SumOfEntropies_DAB_object	Threshold_SumOfEntropies_HE_object	Threshold_SumOfEntropies_nuclei_DAB	Threshold_SumOfEntropies_nuclei_HE	Threshold_WeightedVariance_DAB_object	Threshold_WeightedVariance_HE_object	Threshold_WeightedVariance_nuclei_DAB	Threshold_WeightedVariance_nuclei_HE	URL_EntropyImage	URL_Original	Width_EntropyImage	Width_Original" > ${STAIN}_Image.results.txt

	for AE_NUM in $(ls -d AE*); do 
		echo "* checking data from $AE_NUM ..."
		cat $AE_NUM/cp_output/${STAIN}_Image.txt | tail -n +2 >> ${STAIN}_Image.results.txt
		gzip -vf $AE_NUM/cp_output/${STAIN}_Image.txt
	done
	
	echo ""
	echo "Let's get a-head:" 
	head ${STAIN}_Image.results.txt 
	
	echo ""
	echo "Let's tail that shizzle:" 
	tail ${STAIN}_Image.results.txt 

	echo ""
	echo "Let's get a count of lines:" 
	cat ${STAIN}_Image.results.txt | tail -n +2 | wc -l

	echo ""
	echo "Saving space by gzipping that shizzle ..."
	gzip -vf ${STAIN}_Image.results.txt
	
	echo ""
	echocyan "Collecting data for Experiment."
	# filename: SMA_Experiment.txt
	# Key	Value

	echo "Key	Value" > ${STAIN}_Experiment.results.txt

	for AE_NUM in $(ls -d AE*); do 
		echo "* checking data from $AE_NUM ..."
		cat $AE_NUM/cp_output/${STAIN}_Experiment.txt | tail -n +2 >> ${STAIN}_Experiment.results.txt
		gzip -vf $AE_NUM/cp_output/${STAIN}_Experiment.txt
	done
	
	echo ""
	echo "Let's get a-head:" 
	head ${STAIN}_Experiment.results.txt 
	
	echo ""
	echo "Let's tail that shizzle:" 
	tail ${STAIN}_Experiment.results.txt 

	echo ""
	echo "Let's get a count of lines:" 
	cat ${STAIN}_Experiment.results.txt | tail -n +2 | wc -l

	echo ""
	echo "Saving space by gzipping that shizzle ..."
	gzip -vf ${STAIN}_Experiment.results.txt
	
	echo ""
	echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	echobold "Wow. I'm all done buddy. What a job! let's have a beer!"
	date

### END of if-else statement for the number of command-line arguments passed ###
fi

script_copyright_message
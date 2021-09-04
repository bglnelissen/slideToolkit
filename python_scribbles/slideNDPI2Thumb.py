#!/usr/bin/env python
# script to extract a macro-file from NDPI file

# Also check: https://www.pyimagesearch.com/2019/01/30/macos-mojave-install-tensorflow-and-keras-for-deep-learning/
# pip install importlib-metadata 
# pip install scipy pillow imutils h5py requests progressbar2  scikit-learn scikit-image numpy pandas
# conda install -c anaconda sqlite ncurses readline
# conda install -c bioconda openslide
# conda install -c anaconda scikit-image

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                      slideNDPI2Thumb: NDPI to Thumbnail ")
print("")
print("* Version          : v1.0.0")
print("")
print("* Last update      : 2020-12-28")
print("* Written by       : Nikolas Stathonikos | nstatho2@umcutrecht.nl")
print("* Edited by        : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("")
print("* Description      : This script will get Thumbnails from NDPI images for quick inspection. ")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

### ADD-IN: 
### - requirement check
### - if not present install
### - report that the requirements are met
### - make argument parser
### - put in copyright statement

# import required packages
import sys
import glob
import os
import numpy as np

# for argument parser
import argparse
import textwrap

# to process NDPI images
import openslide
from PIL import Image
import skimage.io
from skimage import img_as_uint

# evaluate arguments
parser = argparse.ArgumentParser(
	prog='slideNDPI2Thumb',
	description='This script will get Thumbnails from NDPI images in a given folderfor quick inspection.',
	usage='slideNDPI2Thumb [-h/--help] -p/--path PATH',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2020 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl; Nikolas Stathonikos | nstatho2@umcutrecht.nl"))
parser.add_argument('-p','--path', help='Give the full path to where the stain directory resides, e.g. /data/isi/d/dhl/ec/VirtualSlides/AE-SLIDES/', required=True)

try:
	args = parser.parse_args()
	print("We are extracting Thumbnails from images in [" + args.path + "].")

except SystemExit:
	print("\nOh, computer says no! You must supply correct arguments when running a *** slideNDPI2Thumb ***!\n")
	parser.print_help()
	exit()

# globals
PATHS = args.path

def extractMacro(slide):
	img = openslide.OpenSlide(slide)
	im = img.associated_images['macro']
# 	tim = img.get_thumbnail(800,600)
	
	# gray scale macro
	# print("* DEBUG: Get gray scaled images.")
	macro_image = np.asarray(im.convert('L'))
	
	# RGB macro
	# print("* DEBUG: Get RGB scaled images.")
	macro_save = np.asarray(im.convert('RGB'))
	
	# RGB macro
	# print("* DEBUG: Get RGB scaled images.")
# 	thumb_save = np.asarray(im.convert())
	
	skimage.io.imsave("{0}.macro.png".format(img._filename), macro_save)
# 	skimage.io.imsave("{0}.thumbnail.png".format(img._filename), thumb_save)
	print("* Exported {0}".format( img._filename + '.[thumbnail/macro].png'))
	return macro_image

print("Starting extractions.")
if __name__ == "__main__":

	directory = PATHS
	for slide in glob.glob(os.path.join(directory, '*.ndpi')):
		macro_image = extractMacro(slide)

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2020 Nikolas Stathonikos, Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands     +")
print("+                                                                                                                 +")
print("+ Permission is hereby granted, free of charge, to any person obtaining a copy of this software and               +")
print("+ associated documentation files (the \"Software\"), to deal in the Software without restriction, including       +")
print("+ without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell         +")
print("+ copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the        +")
print("+ following conditions:                                                                                           +")
print("+                                                                                                                 +")
print("+ The above copyright notice and this permission notice shall be included in all copies or substantial            +")
print("+ portions of the Software.                                                                                       +")
print("+                                                                                                                 +")
print("+ THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT         +")
print("+ LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO       +")
print("+ EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER       +")
print("+ IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR         +")
print("+ THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                                      +")
print("+                                                                                                                 +")
print("+ Reference: http://opensource.org.                                                                               +")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

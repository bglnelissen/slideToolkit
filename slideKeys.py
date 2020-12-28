#!/usr/bin/python
#
# Ref: https://lists.andrew.cmu.edu/pipermail/openslide-users/2015-May/001060.html
#
### ADD-IN: 
### - requirement check
### - if not present install
### - report that the requirements are met
### - get in level count
#
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                      slideKeys: NDPI information ")
print("")
print("* Version          : v1.0.0")
print("")
print("* Last update      : 2020-12-28")
print("* Written by       : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("* Suggested for by : Toby Cornish")
print("")
print("* Description      : This script will get image keys for a given image for quick inspection. ")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# import required packages

import sys
import os

# for argument parser
import argparse
import textwrap

import openslide
from openslide import *

# svsPath = r'_small.svs'

parser = argparse.ArgumentParser(
	prog='slideNDPInfo',
	description='This script will get image keys from a given image in a given folder for quick inspection.',
	usage='slideNDPInfo [-h/--help] -i/--image path_to_image',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2020 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"))
parser.add_argument('-i','--image', help='Give the path to where the image resides, e.g. AE-SLIDES/HE/AE107.HE.ndpi', required=True)

try:
	args = parser.parse_args()
	print("We are extracting information from image [" + args.image + "].")

except SystemExit:
	print("\nOh, computer says no! You must supply correct arguments when running a *** slideNDPInfo ***!\n")
	parser.print_help()
	exit()

# globals
slide = openslide.OpenSlide(args.image)

print('Python version: ',sys.version)
print('OpenSlide version: ',openslide.__version__)
print('OpenSlide library version: ', openslide.__library_version__)
print('Available \'keys\' for image (i.e. \'associated_images.keys\'): ',slide.associated_images.keys())

try:
	macroIm = slide.associated_images['macro']
	print('macro: ',macroIm.size)
except OpenSlideError as macro_error:
	print('error reading macro')
	print(macro_error)

slide.close()

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2020 Toby Cornish, Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands             +")
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

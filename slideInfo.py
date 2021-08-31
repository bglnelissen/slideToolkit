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
print("                                      slideInfo: whole-slide image information ")
print("")
print("* Version          : v1.0.2")
print("")
print("* Last update      : 2021-08-31")
print("* Written by       : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("* Suggested for by : Toby Cornish")
print("")
print("* Description      : This script will get whole-slide image information from (a list of given) images ")
print("                     for quick inspection.")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# import required packages
import numpy as np
import sys
import glob
from pathlib import Path

# for argument parser
import argparse
import textwrap

# for openslide/openCV
import cv2
import os
import openslide
from openslide import *

parser = argparse.ArgumentParser(
	prog='slideNDPInfo',
	description='This script will get whole-slide image information from (a list of given) images for quick inspection.',
	usage='slideNDPInfo [-h/--help] -i/--input.',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2020 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"))
parser.add_argument('-v', '--verbose', help="Will get all available image properties.", default=False, action="store_true")

requiredNamed = parser.add_argument_group('required named arguments')

requiredNamed.add_argument('-i','--input',help="Input (directory containing files). Try: AE107.HE.ndpi or AE-SLIDES/HE/*.ndpi.", nargs="*")

args = parser.parse_args()

if not args.input:
    print("\nOh, computer says no! You must supply correct arguments when running a *** slideMacro ***!")
    print("Note that -i/--input is required. Try: AE107.HE.ndpi or AE-SLIDES/HE/*.ndpi.\n")
    parser.print_help()
    exit()

if len(args.input) > 1:  # bash has sent us a list of files
    files = args.input
else:  # user sent us a wildcard, need to use glob to find files
    files = glob.glob(args.input[0])

# globals

print('Python version: ',sys.version)
print('OpenSlide version: ',openslide.__version__)
print('OpenSlide library version: ', openslide.__library_version__)


for fname in files:
    if args.verbose:
        slide=openslide.OpenSlide(fname)
        print("Showing all image properties for [",fname,"]:")
        for prop_key in slide.properties.keys():
          print("  Property: " + str(prop_key) + ", value: " + str(slide.properties.get(prop_key)))
        
    else:
        slide=openslide.OpenSlide(fname)
        print("Showing some properties for slide [",fname,"] with format: " + str(slide.detect_format(fname)))
        print("Slide associated images:")
        for ai_key in slide.associated_images.keys():
          print("  " + str(ai_key) + ": " + str(slide.associated_images.get(ai_key)))

        macroIm = slide.associated_images['macro']
        img = np.asarray(macroIm)[:,:, 0:3]
        img_size = img.size/1024 # to get kilobytes
        print('* key-image dimensions (height x width in pixels):', img.shape)
        print('* key-image size:', '{:,.2f}'.format(img_size), 'KB') # to get Kb
        print("Slide dimensions: " + str(slide.dimensions))
        objective_power = int(slide.properties[openslide.PROPERTY_NAME_OBJECTIVE_POWER])
        print("Slide objective power: " + str(objective_power))

        print('Available \'levels\': ',slide.level_count)
        print("* level count: %d" % slide.level_count)
        print("* level dimensions: " + str(slide.level_dimensions))
        print("* level downsamples: " + str(slide.level_downsamples))

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

#!/usr/bin/env python
# script to extract a macro images (and display) whole-slide image files (*.TIF, *.NDPI, etc.)
#
# Ref: https://github.com/choosehappy/Snippets/blob/master/extract_macro_level_from_wsi_image_openslide_cli.py
#

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                   slideMacro: extract macro images ")
print("")
print("* Version          : v1.0.1")
print("")
print("* Last update      : 2021-08-31")
print("* Written by       : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("* Inspired by      : choosehappy | https://github.com/choosehappy")
print("")
print("* Description      : This script will get macro-images at a given level of magnification from ")
print("                     (a list of given) images for quick inspection.")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# import required packages
import numpy as np
import glob
from pathlib import Path

# for argument parser
from sys import exit, argv
import argparse
import textwrap

# for openslide/openCV
import cv2
import os
import openslide
from openslide import *

parser = argparse.ArgumentParser(
	prog='slideMacro',
	description='This script will get macro-images at a given level of magnification from (a list of given) images for quick inspection.',
	usage='slideMacro -i/--input -l/--level; optional: -d/--display -o/--outdir -s/--suffix -t/--type -f/--force -v/--verbose; for help: -h/--help',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2020 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"))

parser.add_argument('-d', '--display', help="Also show macro on display, default simply writes macro.", action="store_true")
parser.add_argument('-o', '--outdir', help="Output dir, default is present working directory.", default="./", type=str)
parser.add_argument('-s', '--suffix', help="Suffix to append to end of file, default is 'macro'.", default="", type=str)
parser.add_argument('-t', '--type', help="Output file type, default is png (which is slower), other options are tif.", default="png", type=str)
parser.add_argument('-f', '--force', help="Force utput even if it exists.", default=False, action="store_true")
parser.add_argument('-v', '--verbose', help="While writing images also display image properties.", default=False, action="store_true")

requiredNamed = parser.add_argument_group('required named arguments')

requiredNamed.add_argument('-i','--input',help="Input (directory containing files). Try: *.TIF or /path_to/images/*.ndpi.", nargs="*")
requiredNamed.add_argument('-l','--level',help="Magnification level to extract, with '5' as level 5. Try: 5.")

args = parser.parse_args()

if not args.input:
    print("\nOh, computer says no! You must supply correct arguments when running a *** slideMacro ***!")
    print("Note that -i/--input is required. Try: *.TIF or /path_to/images/*.ndpi.\n")
    parser.print_help()
    exit()

if len(args.input) > 1:  # bash has sent us a list of files
    files = args.input
else:  # user sent us a wildcard, need to use glob to find files
    files = glob.glob(args.input[0])

# make the output directory if it does not exist
if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

for fname in files:
    fnameout=f"{Path(fname).stem}{args.suffix}.!!.{args.type if args.type[0] == '' else ''+args.type}"
    fnameout=Path(args.outdir,fnameout)
    
    if not args.force and os.path.exists(fnameout):
        print(f"Skipping {fnameout} as output file exists and --force is not set")
        continue

    fimage=openslide.OpenSlide(fname)
    
    level = int(args.level)
    img = fimage.read_region((0, 0), level, fimage.level_dimensions[level]) # will get the given level of an image
    img = np.asarray(img)[:,:, 0:3]
    
    if args.display:
        print("Displaying [",fname,"] at level [",level,"].")
        # Let's print each dimension of the image
        print('* image dimensions (height x width in pixels):', img.shape)
        ### FOR DEBUG
#         print('Image data type:', img.dtype)
#         print('Image type:', type(img))
        img_size = img.size/1024 # to get kilobytes
        print('* image size:', '{:,.2f}'.format(img_size), 'KB') # to get Kb
        
        # To display our image variable, we use 'imshow'
        # The first parameter will be title shown on image window
        # The second parameter is the image variable
        # rotate the image for easy reading (https://www.geeksforgeeks.org/python-opencv-cv2-rotate-method/)
        img_r = cv2.rotate(img, cv2.cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow(print('Display image [',fname,'] at level [',level,']'), cv2.cvtColor(img_r, cv2.COLOR_RGB2BGR))
        print('(hit any key on the image to close)') # how waitKey works
        
        # waitKey - ref: https://stackoverflow.com/questions/22274789/cv2-imshow-function-is-opening-a-window-that-always-says-not-responding-pyth
        # 'waitKey' allows us to wait for a key stroke 
        # when a image window is open
        # By leaving it blank it just waits for any key to be 
        # pressed before continuing. 
        # By placing numbers (except 0), we can specify a delay for
        # how long you keep the window open (time is in millisecs here)
        cv2.waitKey()
        # This closes all open windows 
        # Failure to place this will cause your program to hang
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    elif args.verbose:
        print("Processing [",fname,"] at level [",level,"].")
        print('* image dimensions (height x width in pixels):', img.shape)
        img_size = img.size/1024 # to get kilobytes
        print('* image size:', '{:,.2f}'.format(img_size), 'KB') # to get Kb
        cv2.imwrite(str(fnameout).replace("!!","macro"),cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
    else:
        print("Writing macro for [",fname,"] at level [",level,"].")
        cv2.imwrite(str(fnameout).replace("!!","macro"),cv2.cvtColor(img,cv2.COLOR_RGB2BGR))

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2021 Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands                          +")
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

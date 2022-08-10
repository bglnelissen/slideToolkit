#!/usr/bin/env python
# script to display a whole-slide image file and manually rename the file (*.TIF, *.NDPI, etc.)
#
# Ref: https://github.com/choosehappy/Snippets/blob/master/extract_macro_level_from_wsi_image_openslide_cli.py
#

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                   slideRename: display and manually rename images ")
print("")
print("* Version          : v1.0.1")
print("")
print("* Last update      : 2022-08-10")
print("* Written by       : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("* Inspired by      : choosehappy | https://github.com/choosehappy")
print("")
print("* Description      : This script will get thumbnails from (a list of given) images. The user can hit a key and")
print("                     manually type in the correct file name. If the new filename already exists in that ")
print("                     directory the renaming will be cancelled.")
print("                     Note: if the renamed file already exists, an error will occur. Also refer to the  ")
print("                     StackOverflow post:")
print("                     https://stackoverflow.com/questions/30175369/python-program-to-rename-file-names-while-overwriting-if-there-already-is-that-f")
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
	prog='slideRename',
	description='This script will display thumbnails from given images and a terminal window for manual renaming images.',
	usage='slideRename -i/--input; optional: -o/--outdir -s/--suffix -f/--force; for help: -h/--help',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2022 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"))

parser.add_argument('-o', '--outdir', help="Output dir, default is the input image(s) directory.", default="./", type=str)
parser.add_argument('-s', '--suffix', help="Suffix to append to end of file, no suffix will be added by default.", default="", type=str)
parser.add_argument('-f', '--force', help="Force output even if it exists.", default=False, action="store_true")

requiredNamed = parser.add_argument_group('required named arguments')

requiredNamed.add_argument('-i','--input',help="An input image (or directory containing image files) should be given. Try: IMG012.ndpi, *.TIF or /path_to/images/*.ndpi.", nargs="*")

args = parser.parse_args()

if not args.input:
    print("\nOh, computer says no! You must supply correct arguments when running a *** slideRename ***!")
    print("Note that -i/--input is required, i.e. an input image (or directory containing image files) should be given. Try: IMG012.ndpi, *.TIF or /path_to/images/*.ndpi.\n")
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
    
    # this will get the file with the path: os.path.splitext
    # this will get the file name: os.path.basename
    # the [0] will get the first part of the multiple parts
    fname_base = os.path.splitext(os.path.basename(fname))[0]
    fname_base_ext = os.path.splitext(os.path.basename(fname))[1]
    
    if not args.outdir:
    	print("Output directory was not given, set to [",os.path.dirname(fname),"].")
    	fname_base_dir = os.path.dirname(fname)
    else:
    	print("Output directory was given, set to [",args.outdir,"].")
    	fname_base_dir = args.outdir

    fimage=openslide.OpenSlide(fname)
    
    img = fimage.associated_images["macro"] # macro will get the color thumbnail from an image
    img = np.asarray(img)[:,:, 0:3]
    img_r = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    
    print("Displaying [",fname_base,"] at path [",fname_base_dir,"] with extension [",fname_base_ext,"].")
    
    # Let's print each dimension of the image
    print('* image dimensions (height x width in pixels):', img.shape)
    img_size = img.size/1024 # to get kilobytes
    print('* image size:', '{:,.2f}'.format(img_size), 'KB') # to get Kb
    
    # To display our image variable, we use 'imshow'
    # The first parameter will be title shown on image window
    # The second parameter is the image variable
    # rotate the image for easy reading (https://www.geeksforgeeks.org/python-opencv-cv2-rotate-method/)
    cv2.imshow(print('Display image [',fname_base,']'), cv2.cvtColor(img_r, cv2.COLOR_RGB2BGR))
    print('(hit any key on the image to close)') # how waitKey works

    # waitKey - ref: https://stackoverflow.com/questions/22274789/cv2-imshow-function-is-opening-a-window-that-always-says-not-responding-pyth
    # 'waitKey' allows us to wait for a key stroke 
    # when a image window is open
    # By leaving it blank it just waits for any key to be 
    # pressed before continuing. 
    # By placing numbers (except 0), we can specify a delay for
    # how long you keep the window open (time is in millisecs here)
    cv2.waitKey(0)
    
    # Rename file
    # here the user can manually rename the file
    # ask for filename if non is existing (by typing or by barcode)
    # This is bash-code and needs to be edited to python
    old_fname = fname_base
    
    new_fname = input("Enter slide name: ")
    print("You entered: " + new_fname)

    old_fnameout=f"{fname_base_dir}/{old_fname}{fname_base_ext}"
    new_fnameout=f"{fname_base_dir}/{new_fname}{fname_base_ext}"

    # This closes all open windows 
    # Failure to place this will cause your program to hang
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    
    if not args.force and os.path.exists(new_fnameout):
    	print(f"Skipping {new_fnameout} as output file exists and --force is not set")
    	continue

    print("Processing [",fname,"].")
    print('* image dimensions (height x width in pixels):', img.shape)
    img_size = img.size/1024 # to get kilobytes
    print('* image size:', '{:,.2f}'.format(img_size), 'KB') # to get Kb
    os.rename(old_fnameout, new_fnameout)

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2022 Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands                          +")
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

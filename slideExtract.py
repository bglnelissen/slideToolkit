#!/usr/bin/env python
# script to extract a macro-file from NDPI file
#
# Ref: https://github.com/choosehappy/Snippets/blob/master/extract_macro_level_from_wsi_image_openslide_cli.py
#

print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                slideExtract: extract thumbnails and macro-images ")
print("")
print("* Version          : v1.0.0")
print("")
print("* Last update      : 2020-12-28")
print("* Written by       : choosehappy | https://github.com/choosehappy")
print("* Edited by        : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("")
print("* Description      : This script will get thumbnails and macro images from (a list of given) images ")
print("                     for quick inspection.")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

import numpy as np
import cv2
import glob

# for argument parser
import argparse
import textwrap

from pathlib import Path
import os
import openslide

from PIL import Image
import matplotlib.pyplot as plt

# 
parser = argparse.ArgumentParser(
	prog='slideExtract',
	description='This script will get thumbnails and macro images from given images for quick inspection.',
	usage='slideExtract [-h/--help] -i/--input -/--levels -o/--outdir -s/--suffix -t/--type -f/--force',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2020 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"))

parser.add_argument('-i','--input',help="Input (directory containing files). Try: *.TIF or /path_to/images/*.ndpi.", nargs="*")
parser.add_argument('-l','--levels',help="Comma seperated list of levels to extract, with 'm' as thumbnail and '6' as level 6. Try: m,6. REQUIRED", required=True)
parser.add_argument('-o', '--outdir', help="Output dir, default is present working directory.", default="./", type=str)
parser.add_argument('-s', '--suffix', help="Suffix to append to end of file, default is 'thumb' for thumbnail and 'macro' for a given level.", default="", type=str)
parser.add_argument('-t', '--type', help="Output file type, default is tif, other options are png (which is slow).", default="tif", type=str)
parser.add_argument('-f', '--force', help="Force utput even if it exists.", default=False, action="store_true")

try:
    args = parser.parse_args()
    print("We are extracting thumbnails and macro images.")
except SystemExit:
    print("\nOh, computer says no! You must supply correct arguments when running a *** slideExtract ***!\n")
    parser.print_help()
    exit()

args = parser.parse_args()

if len(args.input) > 1:  # bash has sent us a list of files
    files = args.input
else:  # user sent us a wildcard, need to use glob to find files
    files = glob.glob(args.input[0])

if not os.path.exists(args.outdir):
    os.makedirs(args.outdir)

for fname in files:
    fnameout=f"{Path(fname).stem}{args.suffix}.!!.{args.type if args.type[0] == '' else ''+args.type}"
    fnameout=Path(args.outdir,fnameout)
    
    if not args.force and os.path.exists(fnameout):
        print(f"Skipping {fnameout} as output file exists and --force is not set")
        continue

    fimage=openslide.OpenSlide(fname)
    
    for level in args.levels.split(","):
        if level == 'm': 
            img = fimage.associated_images["macro"]
        else:
            level = int(level)
#             img = fimage.read_region((0, 0), level, fimage.level_dimensions[level])
        img = np.asarray(img)[:,:, 0:3]
        
        # Let's print each dimension of the image
        print('Image dimensions (height x width in pixels):', img.shape)
        print('Image data type:', img.dtype)
        print('Image type:', type(img))
        print('Image size:', img.size)
        
        # To display our image variable, we use 'imshow'
        # The first parameter will be title shown on image window
        # The second parameter is the image variable
        cv2.imshow('Display image]', cv2.cvtColor(img[731, 2164], cv2.COLOR_RGB2BGR))
        
        # 'waitKey' allows us to wait for a key stroke 
        # when a image window is open
        # By leaving it blank it just waits for any key to be 
        # pressed before continuing. 
        # By placing numbers (except 0), we can specify a delay for
        # how long you keep the window open (time is in millisecs here)
        cv2.waitKey(3)
        
        # This closes all open windows 
        # Failure to place this will cause your program to hang
        cv2.destroyAllWindows() 
#         cv2.imwrite(str(fnameout).replace("!!",str(level)),cv2.cvtColor(img,cv2.COLOR_RGB2BGR))
#         cv2.imwrite(str(fnameout).replace("!!","Thumb"),cv2.cvtColor(thumb_image,cv2.COLOR_RGB2BGR))
#         cv2.imwrite(str(fnameout).replace("!!","macro"),cv2.cvtColor(img,cv2.COLOR_RGB2BGR))


print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2020 choosehappy, Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands             +")
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

#!/usr/bin/env python3
# script to extract a thumbnails and macros whole-slide image files (*.TIF, *.NDPI, etc.)
#
# Ref: https://github.com/choosehappy/Snippets/blob/master/extract_macro_level_from_wsi_image_openslide_cli.py
#

"""
    slideExtract
    This script is designed to extract thumbnails and macro-images from whole-slide image (WSI) files, 
    such as TIF or NDPI files. The script uses the OpenSlide library to handle WSI and OpenCV for image processing.

    Usage:
    python slideExtract.py -i/--input -l/--levels; optional: -d/--display -o/--outdir -s/--suffix -t/--type -f/--force -v/--verbose; for help: -h/--help

    Example usage:
    python slideExtract.py -i IMG012.ndpi -l m,6

    Arguments:
    --input, -i     Input (directory containing files). Try: IMG012.ndpi (or *.TIF or /path_to/images/*.ndpi).
    ---levels, -l   Comma separated list of magnification levels to extract, with 'm' as thumbnail and '6' as level 6. Try: m,6.
    ---display, d   Display the image. Optional.
    ---outdir, -o   Output directory. Optional.
    ---suffix, -s   Suffix to append to end of file, default is 'm' for thumbnail and '#' for a given level. Optional.
    ---type, -t     Output file type, default is png (which is slower), other options are tif. Optional.
    ---force, -f    Force output even if it exists. Optional.
    ---verbose, -v  While writing images also display image properties. Optional.
    ---debug, -de   Debug mode. Optional.
    ---version, -V  Print version number and exit.
    ---help, -h     Print help.

"""

# Version information
VERSION_NAME = 'slideExtract'
VERSION = '1.0.5'
VERSION_DATE = '2023-01-08'
COPYRIGHT = 'Copyright 1979-2024. Sander W. van der Laan | s.w.vanderlaan [at] gmail [dot] com | https://vanderlaanand.science.'
COPYRIGHT_TEXT = f'\nThe MIT License (MIT). \n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and \nassociated documentation files (the "Software"), to deal in the Software without restriction, \nincluding without limitation the rights to use, copy, modify, merge, publish, distribute, \nsublicense, and/or sell copies of the Software, and to permit persons to whom the Software is \nfurnished to do so, subject to the following conditions: \n\nThe above copyright notice and this permission notice shall be included in all copies \nor substantial portions of the Software. \n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR \nPURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS \nBE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, \nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE \nOR OTHER DEALINGS IN THE SOFTWARE. \n\nReference: http://opensource.org.'

# import required packages
import numpy as np
import glob
from pathlib import Path

# for argument parser
import argparse
from argparse import RawTextHelpFormatter
import textwrap

# for openslide/openCV
import cv2
import os
import openslide
from openslide import *

# Define main function
def main():
    parser = argparse.ArgumentParser(description=f'''
+ {VERSION_NAME} v{VERSION} +

slideExtract
This script is designed to extract thumbnails and macro-images from whole-slide image (WSI) files, 
such as TIF or NDPI files. The script uses the OpenSlide library to handle WSI and OpenCV for image processing.

Usage:
python slideExtract.py -i/--input -l/--levels; optional: -d/--display -o/--outdir -s/--suffix -t/--type -f/--force -v/--verbose; for help: -h/--help

Example usage:
python slideExtract.py -i IMG012.ndpi -l m,6
        ''',
        epilog=f'''
+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} \n{COPYRIGHT_TEXT}+''', 
        formatter_class=argparse.RawTextHelpFormatter)
    requiredNamed = parser.add_argument_group('required named arguments')

    requiredNamed.add_argument('-i','--input', help="Input (directory containing files). Try: IMG012.ndpi (or *.TIF or /path_to/images/*.ndpi).", nargs="*")#, required=True)
    requiredNamed.add_argument('-l','--levels', help="Comma separated list of magnification levels to extract, with 'm' as thumbnail and '6' as level 6. Try: m,6.")#, required=True)
    parser.add_argument('-o', '--outdir', help="Output dir, default is present working directory.", default="<<SAME>>", type=str)
    parser.add_argument('-s', '--suffix', help="Suffix to append to end of file, default is 'm' for thumbnail and '#' for a given level.", default="", type=str)
    parser.add_argument('-t', '--type', help="Output file type, default is png (which is slower), other options are tif.", default="png", type=str)
    parser.add_argument('-f', '--force', help="Force output even if it exists.", default=False, action="store_true")
    parser.add_argument('-v', '--verbose', help="While writing images also display image properties.", default=False, action="store_true")
    parser.add_argument('-de', '--debug', help="Debug mode.", default=False, action="store_true")
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {VERSION} ({VERSION_DATE}).')

    args = parser.parse_args()

    if not args.input or not args.levels:
        print("\nOh, computer says no! You must supply correct arguments when running a *** slideExtract ***!")
        print("Note that -i/--input and -l/--levels are required. Try: --input IMG012.ndpi (or *.TIF or /path_to/images/*.ndpi) --level m,6.\n")
        parser.print_help()
        exit()

    # Start the script
    print(f"+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}) +")
    print(f"\nExtract thumbnails and macro images from WSI file(s).\n")
    if len(args.input) > 1:  # bash has sent us a list of files
        if args.verbose:
            print("Processing multiple files.")
        files = args.input
    else:  # user sent us a wildcard, need to use glob to find files
        if args.verbose:
            print("Processing wildcard to find matching files or a specific file.")
        files = glob.glob(args.input[0])

    for fname in files:
        # Creating the output directory. By default it will write to the input directory;
        # that is to say, the directory given after -i/--input.
        if args.outdir == "<<SAME>>":
            if args.verbose:
                print("Output directory set to [",os.path.dirname(os.path.realpath(fname)),"].\n")
            args.outdir = os.path.dirname(os.path.realpath(fname))
        else:
            if args.verbose:
                print("Output directory set to [",args.outdir,"].\n")
            os.makedirs(args.outdir, exist_ok=True)

        # Creating the output filename. By default it will write to the input filename; 
        # that is to say, the filename given after -i/--input.
        # Extract file name without extension
        fname_base = Path(fname).stem

        # Create the output filename with optional suffix and type
        fname_suffix = args.suffix if args.suffix else ''
        fname_type = args.type if args.type else ''
        fnameout = f"{fname_base}{fname_suffix}.LEVEL.{fname_type}"

        fnameout=os.path.join(args.outdir,fnameout)

        # Open the file and extract the image
        fimage=openslide.OpenSlide(fname)
        
        # Extract the image
        for level in args.levels.split(","):
            # set the level
            if level == 'm':
                if args.verbose:
                    print("Processing [",fname,"] at thumbnail level (m).")
                img = fimage.associated_images["macro"]
                if args.debug:
                    print(f">>> Debug. Checking if thumbnail exists: ", os.path.join(args.outdir,f"{fname_base}{fname_suffix}.{level}.{fname_type}"))
                if not args.force and os.path.exists(os.path.join(args.outdir,f"{fname_base}{fname_suffix}.{level}.{fname_type}")):
                    print(f"Skipping thumbnail exists and --force is not set")
                    continue
            else:
                if args.verbose:
                    print("Processing [",fname,"] at level [",level,"].")
                level = int(level)
                img = fimage.read_region((0, 0), level, fimage.level_dimensions[level])
                if args.debug:
                    print(f">>> Debug. Checking if macro file exists: ", os.path.join(args.outdir,f"{fname_base}{fname_suffix}.{level}.{fname_type}"))
                if not args.force and os.path.exists(os.path.join(args.outdir,f"{fname_base}{fname_suffix}.{level}.{fname_type}")):
                    print(f"Skipping macro file exists and --force is not set")
                    continue
            img = np.asarray(img)[:,:, 0:3]

            # Display information about the image
            if args.verbose:
                print('* image dimensions (height x width in pixels):', img.shape)
                img_size = img.size/1024 # to get kilobytes
                print('* image size:', '{:,.2f}'.format(img_size), 'KB') # to get Kb
                print("Writing image for [",fname,"] at level [",level,"].\n")
            # Write the image
            cv2.imwrite(str(fnameout).replace("LEVEL",str(level)),cv2.cvtColor(img,cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    main()

# Print the version number
print(f"\n+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}). {COPYRIGHT} +")
print(f"{COPYRIGHT_TEXT}")
# End of file
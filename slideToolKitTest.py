#!/usr/bin/python
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("                                   slideToolKitTest: test the environment ")
print("")
print("* Version          : v1.0.0")
print("")
print("* Last update      : 2021-11-06")
print("* Written by       : Sander W. van der Laan | s.w.vanderlaan@gmail.com")
print("")
print("* Description      : This script will test the slideToolKit virtual environment.")
print("")
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

# import required packages
import sys
import time
import arrow
import datetime

# for argument parser
import argparse
import textwrap

# for openslide/openCV
import cv2
import os
import openslide
from openslide import *

utc = arrow.utcnow()

# argument parser
parser = argparse.ArgumentParser(
	prog='slideToolKitTest',
	description='This script will test the slideToolKit virtual environment.',
	usage='slideToolKitTest [-h/--help] -b/--bdate.',
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog=textwrap.dedent("Copyright (c) 1979-2021 Sander W. van der Laan | s.w.vanderlaan@gmail.com"))
parser.add_argument('-v', '--verbose', help="Will get all available image properties.", default=False, action="store_true")
parser.add_argument('-b','--bdate',help="Your birthdate - format YYYY-MM-DD. Try: 1979-01-13.", 
#                     required=True, 
                    type=datetime.date.fromisoformat) # make sure that the date format is correct, if not the program will stop

args = parser.parse_args()

if not args.bdate:
    print("\nOh, computer says no! You must supply correct arguments when running a *** slideToolKitTest ***!")
    print("Note that -b/--bdate is required. Try: 1979-01-13.\n")
    parser.print_help()
    exit()

bd = args.bdate 
print("Printing the installed versions.")
print('* Python version: ',sys.version)
print('* OpenSlide version: ',openslide.__version__)
print('* OpenSlide library version: ', openslide.__library_version__)

print("\nTesting the argument parsing of your birth date.")
print(f"UTC time is = {utc}")
pacific = utc.to('Europe/Vatican') #https://pvlib-python.readthedocs.io/en/stable/timetimezones.html
print(f"European/Amsterdam time is = {pacific}")
bdate_text='You were born on ' + str(bd) # make a string out of the date
birth_date = arrow.get(bdate_text, 'YYYY-MM-DD') # arrow() will get the date from a text
print(f"Your birth date is {birth_date}.")
print(f"You were born {birth_date.humanize()}.")

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("+ The MIT License (MIT)                                                                                           +")
print("+ Copyright (c) 1979-2021 Sander W. van der Laan | UMC Utrecht, Utrecht, the Netherlands                          +")
print("+                                                                                                                 +")
print("+ Permission is hereby granted, free of charge, to any person obtaining a copy of this software and               +")
print("+ associated documentation files (the \"Software\"), to deal in the Software without restriction, including         +")
print("+ without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell         +")
print("+ copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the        +")
print("+ following conditions:                                                                                           +")
print("+                                                                                                                 +")
print("+ The above copyright notice and this permission notice shall be included in all copies or substantial            +")
print("+ portions of the Software.                                                                                       +")
print("+                                                                                                                 +")
print("+ THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT           +")
print("+ LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO       +")
print("+ EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER       +")
print("+ IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR         +")
print("+ THE USE OR OTHER DEALINGS IN THE SOFTWARE.                                                                      +")
print("+                                                                                                                 +")
print("+ Reference: http://opensource.org.                                                                               +")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")


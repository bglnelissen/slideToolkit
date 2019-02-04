# imports
import os
import shutil
import argparse
import textwrap
import datetime
NOWTIME = datetime.datetime.now()
# print NOWTIME.year, NOWTIME.month, NOWTIME.day, NOWTIME.hour, NOWTIME.minute, NOWTIME.second

# evaluate arguments
parser = argparse.ArgumentParser(
    prog='slideCopy',
    description='This script copies images of a given stain from the BULK in series starting from a given lower to an upper bound.',
    usage='slideCopy [-h/--help] -l/--lower LOWER -u/--upper UPPER -s/--stain STAIN',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent("\nCopyright (c) 2018-2019 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl; \nTim G.M. van de Kerkhof | t.g.m.vandekerkhof@umcutrecht.nl."))
parser.add_argument('-l','--lower', help='Give the lower bound of the folder to copy, e.g. 1.', type=int, required=True)
parser.add_argument('-u','--upper', help='Give the upper bound of the folder to copy, e.g. 100.', type=int, required=True)
parser.add_argument('-s','--stain', help='Give the name of the stain, e.g. CD34.', required=True)

try:
    args = parser.parse_args()
    print("We are copying files for stain [" + args.stain + "] from series [" + args.lower + "-" + args.upper + "].\n")

except SystemExit:
    print("\033[1;31m \nOh, computer says no! You must supply correct arguments when running a *** slideCopy ***!\n")
    parser.print_help()
    exit()

# Set vars for batch
lower = args.lower
upper = args.upper
batch = True
STAIN = args.stain
basedir = "/data/isi/d/dhl/ec/VirtualSlides/AE-SLIDES/"+STAIN+"/_"

# folder = argv[1]
# dest = argv[2]

#if batch == False:
#	for filename in os.listdir(folder):
#		shutil.copy(folder+"/"+filename,dest)
if batch == True:
	for i in range(lower, upper+1):
		for filename in os.listdir(basedir+str(i)+"/"):
			shutil.copy(basedir+str(i)+"/"+filename,"/hpc/dhl_ec/VirtualSlides/"+STAIN+"/")		
			print(filename)
# 			print(i)

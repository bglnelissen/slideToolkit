# imports
import glob
import shutil
import os
import argparse
import textwrap
import datetime
NOWTIME = datetime.datetime.now()
# print NOWTIME.year, NOWTIME.month, NOWTIME.day, NOWTIME.hour, NOWTIME.minute, NOWTIME.second

# evaluate arguments
parser = argparse.ArgumentParser(
    prog='slideProcessor',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent("Copyright (c) 2018-2019 Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl; Tim G.M. van de Kerkhof | t.g.m.vandekerkhof@umcutrecht.nl."))
parser.add_argument('-s','--stain', help='Give the name of the stain, e.g. CD34', required=True)
parser.add_argument('-p','--path-to-stains', help='Give the full path to where the stain directory resides, e.g. /data/isi/d/dhl/ec/VirtualSlides/AE-SLIDES/', required=True)

try:
    args = parser.parse_args()
#     print("We are moving files for stain [" + args.stain + "] in [" args.path_to_stains + "].")

except SystemExit:
    print("Oh, computer says no! You must supply correct arguments when running a *** slideProcessor ***!")
    parser.print_help()

# globals
STAIN = args.stain
PATHS = args.path_to_stains + "/" + STAIN
BASE = PATHS + "/_"

TIFnames = glob.glob(PATHS+"/*.TIF")
NDPInames = glob.glob(PATHS+"/*.ndpi")

counter = 0
basenum = 1
for tif in TIFnames:
    if counter == 10:
        basenum += 1
        counter = 0
    if not os.path.exists(BASE+str(basenum)):
        os.makedirs(BASE+str(basenum))
#     print(BASE+str(basenum)+"/"+tif)
    filename = tif.rsplit('/',1)
    shutil.move(tif, BASE+str(basenum)+"/"+str(filename[1]))
    counter += 1
    

for tif in NDPInames:
    if counter == 10:
        basenum += 1
        counter = 0
    if not os.path.exists(BASE+str(basenum)):
        os.makedirs(BASE+str(basenum))
#     print(BASE+str(basenum)+"/"+tif)
    filename = tif.rsplit('/',1)
    shutil.move(tif, BASE+str(basenum)+"/"+str(filename[1]))
    counter += 1

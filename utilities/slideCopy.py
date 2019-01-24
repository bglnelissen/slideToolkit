# imports
import os
import shutil
from sys import argv

# vars for batch
lower = 1
upper = 100
batch = True
STAIN = "HE"
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
			print(i)

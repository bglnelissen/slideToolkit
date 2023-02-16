import glob
import os
import shutil
from sys import argv


bulkPathBaseAE = "/data/isi/d/dhl/ec/VirtualSlides/AE-SLIDES/"

stainHPC = argv[1]
stainBulk = argv[2]
XNum = argv[3]
subDir = argv[4]
copy = argv[5]
filepath = (stainHPC+"/failed_slides/AEprocesslist.txt")

checkList = []

for i in glob.glob(stainHPC + "/" + XNum + "*/" + subDir):
	if not os.listdir(i):
		checkList.append(i)

print("total number of unprocessed slides: " + str(len(checkList)))

if not os.path.exists(stainHPC + "/failed_slides"):
	os.makedirs(stainHPC + "/failed_slides")

copyList = []
if copy == "y":
	if XNum == "AE":
		print("Using AE")
		for slide in checkList:
			slide = slide.split("/")[-2]
			if not glob.glob(stainHPC + "/failed_slides/" + slide + "*"):
				copyList.append(glob.glob(bulkPathBaseAE  + stainBulk + "/" + slide + "*")[0])
	print("now copying " + str(len(copyList)) + " slides that remain from the total") 

	if copyList:
		with open(filepath, 'w') as f:
			for origfile in copyList:
				print("now copying " + origfile + " to failed slides file")
			
				f.write("%s\n" % origfile)


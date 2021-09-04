import os
import shutil
import glob
from sys import argv

stainPath = argv[1]

for i in glob.glob(stainPath + "_[0-9]*"):
	for j in glob.glob(i+"/*"):
		shutil.move(j, stainPath)
		print(j)
	os.rmdir(i)

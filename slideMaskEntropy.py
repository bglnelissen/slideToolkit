#!/usr/local/bin/python

print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
print "                             slideToolkit Entropy Filter"
print "                                     version 1.0"
print ""
print "* Written by         : Tim Bezemer"
print "* E-mail             : t.bezemer-2@umcutrecht.nl"
print "* Suggested for by   : Sander W. van der Laan | s.w.vanderlaan-2@umcutrecht.nl"
print "* Last update        : 2016-08-12"
print "* Version            : 1.2.20160812"
print ""
print "* Description        : Makes maskers of PNG files using a entropy-filter. To be"
print "                       used when the regular mask-making program (slideMask)"
print "                       is insufficient."
print ""
print "* USAGE:               for DIR in $(ls) ; do echo \"* Processing [ \"$DIR\" ]...\"; $(command -v slideMaskEntropy.py) \"$DIR\"/\"$DIR\".macro.png; done"
print "                       slideMaskEntropy.py [FILE.png]"
print ""
print ""
print "* PREREQUISITES: The packages 'scikit-image', 'numpy', and 'matplotlib' are required."
print "                 Installation instructions:"
print "                 pip install numpy"
print "                 pip install matplotlib"
print "                 pip install scikit-image"
print ""
print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from skimage import data
from skimage.filters.rank import entropy
from skimage.morphology import disk
from skimage.util import img_as_ubyte
from skimage.io import imread, imsave

from sys import exit
from sys import argv
import os.path

import numpy as np

import warnings
warnings.filterwarnings("ignore")


def filter_entropy_image(image, filter):
	
	eimage = entropy(image, disk(5))

	new_picture =  np.ndarray(shape=eimage.shape) #[[False] * image.shape[1]] * image.shape[0]

	for rn, row in enumerate(eimage):
	
		for pn, pixel in enumerate(row):

			if pixel < filter:
				
				new_picture[rn,pn] = True

			else:
				new_picture[rn,pn] = False

	return new_picture.astype('b')

fn = argv[1]

if not os.path.isfile(fn):
	print "No such file"
	sys.exit()


print "\tCreating tissue mask (entropy filter)..."

image = imread(fn, True)

entropy_image = filter_entropy_image(image, 3.5)

plt.axis('off')

newfile = fn

newfile = newfile.replace(".macro.png", ".newmask.png")

#np.save(newfile, entropy_image)

plt.imsave(newfile, entropy_image, cmap=plt.cm.binary)

print "\t>>> Saved image as:" + newfile


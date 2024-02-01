#!/usr/bin/env python3

"""
slideEntropySegmentation
(https://github.com/CirculatoryHealth/EntropyMasker)

This script makes use of EntropyMasker to create a mask for the given sample image.
The resulting mask is saved in the given masking directory.

Usage:
python slideEntropySegmentation.py --input_img path/to/image.ndpi --masks_dir path/to/masks/dir/

Options:
    --input_img         Specify the path to the input image (_ndpi or _tif). Required.
    --masks_dir         Specify the path to the masking directory. Required.
"""

# Version information
VERSION_NAME = 'slideEntropySegmentation'
VERSION = '1.0.0'
VERSION_DATE = '2024-01-019'
COPYRIGHT = 'Copyright 1979-2023. Tim S. Peters & Sander W. van der Laan | s.w.vanderlaan [at] gmail [dot] com | https://vanderlaanand.science.'
COPYRIGHT_TEXT = f'\nThe MIT License (MIT). \n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and \nassociated documentation files (the "Software"), to deal in the Software without restriction, \nincluding without limitation the rights to use, copy, modify, merge, publish, distribute, \nsublicense, and/or sell copies of the Software, and to permit persons to whom the Software is \nfurnished to do so, subject to the following conditions: \n\nThe above copyright notice and this permission notice shall be included in all copies \nor substantial portions of the Software. \n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR \nPURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS \nBE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, \nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE \nOR OTHER DEALINGS IN THE SOFTWARE. \n\nReference: http://opensource.org.'

# Import required packages
from copy import deepcopy
import openslide
import argparse
from skimage.morphology import disk, remove_small_objects
from skimage.filters.rank import entropy
from scipy.signal import argrelextrema
import numpy as np
import time
import cv2
import os
import sys

# parser = argparse.ArgumentParser('entropyMasker')
parser = argparse.ArgumentParser(description=f'''
+ {VERSION_NAME} v{VERSION} +

This script makes use of EntropyMasker to create a mask for the given sample image.

"EntropyMasker is a fully automated approach for separating foreground (tissue) and background 
in bright-field microscopic whole-slide images of (immuno)histologically stained samples. This 
method is unaffected by changes in scanning or image processing conditions, by using a measure 
of local entropy and generating corresponding binary tissue masks."
- https://github.com/CirculatoryHealth/EntropyMasker

Example usage:
python slideEntropySegmentation.py --input_img path/to/image.ndpi --masks_dir path/to/masks/dir/
        ''',
        epilog=f'''
+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} \n{COPYRIGHT_TEXT}+''', 
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--input_img', help='path to WSI image', type=str, required=True)
parser.add_argument('--masks_dir', help='path to directory to save mask image', type=str, required=True)
args = parser.parse_args()

# function to apply the entropy mask/filter
def filter_entropy_image(image, filter, disk_radius=3):

    eimage = entropy(image, disk(disk_radius))
    # [[False] * image.shape[1]] * image.shape[0]
    new_picture = np.ndarray(shape=eimage.shape)
    for rn, row in enumerate(eimage):
        for pn, pixel in enumerate(row):
            if pixel < filter:
                new_picture[rn, pn] = True
            else:
                new_picture[rn, pn] = False
    return new_picture.astype('b')

# main entropyMasker program to apply to a given image
def entropyMasker():

    # Slide name without extension
    slidename_noext = args.input_img.split('/')[-1].rsplit('.', 1)[0]

    print(f'Processing {slidename_noext}')

    os.makedirs(args.masks_dir, exist_ok=True)
    savename = os.path.join(args.masks_dir, slidename_noext + '.jpg')

    if not os.path.exists(savename):
        try:
            slide_opened = openslide.OpenSlide(args.input_img)
            img_RGB = np.asarray(slide_opened.read_region(
                (0, 0), 4, slide_opened.level_dimensions[4]))[:, :, 0:3]
            img = cv2.cvtColor(img_RGB, cv2.COLOR_RGB2GRAY)
            source = deepcopy(img)/255.0

            # ORO = cv2.imread(slide, 0)
            # source = deepcopy(ORO)
            # cv2.imshow("test", source)
            # cv2.waitKey()
            ent = entropy(source, disk(5))
            hist = list(np.histogram(ent, 30))
            minindex = list(argrelextrema(hist[0], np.less))

            for i in range(len(minindex[0])):
                temp_thresh = hist[1][minindex[0][i]]
                if temp_thresh > 1 and temp_thresh < 4:
                    thresh_localminimal = temp_thresh

            thresh1 = (255*filter_entropy_image(img,
                                                thresh_localminimal)).astype('uint8')
            mask_255 = cv2.bitwise_not(deepcopy(thresh1))

            # Add erosion and dialation operations
            mask_255 = remove_small_objects(mask_255 == 255, 50**2)
            mask_255 = (mask_255*255).astype(np.uint8)
            mask_255 = cv2.morphologyEx(
                mask_255, cv2.MORPH_CLOSE, kernel=np.ones((50, 50), np.uint8))

            print(
                "Writing entropy-based masked image at [", savename, "].")

            cv2.imwrite(savename, mask_255)
        except Exception as e:
            print(e, 'Skipped slide', slidename_noext)
    else:
        print(f'Already existing mask found for {slidename_noext}: {savename}')


if __name__ == '__main__':
    t = time.time()
    entropyMasker()
    print('Tissue segmentation done (%.2f)' % (time.time() - t))

# Print the version number
print(f"\n+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}). {COPYRIGHT} +")
print(f"{COPYRIGHT_TEXT}")
# End of file
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

parser = argparse.ArgumentParser('entropyMasker')
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

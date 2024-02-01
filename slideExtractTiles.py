#!/usr/bin/env python3

"""
slideExtractTiles

This script takes an input image and mask and extracts tiles from it. The default tile size
is 2000 x 2000. It outputs the tiles and an overview image, overlaying the saved tiles.

Usage:
python slideExtractTiles.py --layer 1 --tile_size 2000 --file path/to/image.ndpi --mask path/to/image_mask.jpg --out path/to/out/dir

Options:
    --file              Path to the input image. Required.
    --mask              Path to masks accompanying image. Required.
    --out               Path to output directory. Optional.
    --layer             Parameter determining at which layer to extract tiles. Optional.
    --tile_size         Size of tiles. Optional.
    --suffix            Additional output folder suffix. Optional.
    --save_mask         Save resized mask. Optional.
    --keep_empty        Keep empty tiles after masking. Optional.
    --save_thumbnail    Keep thumbnail image after masking. Optional.
    --color             Masking color (w=white, b=black). Optional.
"""

# Version information
VERSION_NAME = 'slideExtractTiles'
VERSION = '1.0.0'
VERSION_DATE = '2024-01-19'
COPYRIGHT = 'Copyright 1979-2023. Tim S. Peters & Sander W. van der Laan | s.w.vanderlaan [at] gmail [dot] com | https://vanderlaanand.science.'
COPYRIGHT_TEXT = f'\nThe MIT License (MIT). \n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and \nassociated documentation files (the "Software"), to deal in the Software without restriction, \nincluding without limitation the rights to use, copy, modify, merge, publish, distribute, \nsublicense, and/or sell copies of the Software, and to permit persons to whom the Software is \nfurnished to do so, subject to the following conditions: \n\nThe above copyright notice and this permission notice shall be included in all copies \nor substantial portions of the Software. \n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, \nINCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR \nPURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS \nBE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, \nTORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE \nOR OTHER DEALINGS IN THE SOFTWARE. \n\nReference: http://opensource.org.'

# Import required packages
from torch.utils.data import Dataset, DataLoader
from PIL import Image, ImageDraw
import argparse
import openslide
import os
import math
import datetime
import numpy as np
from numpy import asarray
import cv2
import imageio.v2 as imageio
from matplotlib import pyplot as plt

Image.MAX_IMAGE_PIXELS = None

# parser = argparse.ArgumentParser('extract_tiles')
parser = argparse.ArgumentParser(description=f'''
+ {VERSION_NAME} v{VERSION} +

This script takes an input image and mask and extracts tiles from it. The default tile size
is 2000 x 2000. It outputs the tiles and an overview image, overlaying the saved tiles.

Example usage:
python slideExtractTiles.py --layer 1 --tile_size 2000 --file path/to/image.ndpi --mask path/to/image_mask.jpg --out path/to/out/dir
        ''',
        epilog=f'''
+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} \n{COPYRIGHT_TEXT}+''', 
        formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--file', help='path to slide image')# Input slide
parser.add_argument('--mask', help='path to slide image')# Input mask
parser.add_argument('--out', default='./', help='path to output directory')# Out dir
parser.add_argument('--layer', type=int, default=0, help='At which layer to extract tiles')# slide layer to extract tiles
parser.add_argument('--tile_size', type=int, default=2000, help='Size of tiles')# size of tiles
parser.add_argument('--suffix', default="", help='Additional output folder suffix')# output suffix
parser.add_argument('--save_mask', type=bool, default=False, help='Save resized mask')# output resized mask
parser.add_argument('--keep_empty', type=bool, default=False, help='Keep emty tiles after masking')# output resized mask
parser.add_argument('--save_thumbnail', type=bool, default=True, help='Keep thumbnail image after masking')# save thumbnail image
parser.add_argument('--color', default="w", help='Masking color (w=white, b=black)')# masking color
args = parser.parse_args()


class Whole_Slide_Bag(Dataset):

    def __init__(self, slide, tile_size, mask):

        # slide : openslide WSI
        # tile_size : dimension of each squared patch
        # transform : transform function for the tiles classification model
        # fe_transf : transform function for the features extraction model

        self.slide = slide
        self.dimensions = (
            slide.level_dimensions[args.layer][0], slide.level_dimensions[args.layer][1])
        self.cols = np.arange(
            0, int(self.dimensions[0]/tile_size) * tile_size, tile_size)
        self.rows = np.arange(
            0, int(self.dimensions[1]/tile_size) * tile_size, tile_size)
        self.length = len(self.cols) * len(self.rows)
        self.tile_size = tile_size
        self.mask = mask

    def __len__(self):
        return self.length

    def __getitem__(self, idx):

        row = self.rows[math.floor(idx/len(self.cols))]
        col = self.cols[idx % len(self.cols)]

        tile_row = row
        tile_col = col
        # tile_mask = self.mask[tile_col: tile_col + self.tile_size //
        #                       self.scale_factor, tile_row: tile_row + self.tile_size // self.scale_factor]
        tile_mask = self.mask[tile_row: tile_row +
                              self.tile_size, tile_col: tile_col + self.tile_size]
        res = (tile_mask == 255).sum() / \
            (tile_mask.shape[0]*tile_mask.shape[1])

        return (col, row), res, tile_mask


def slide_to_scaled_pil_image(slide, SCALE_FACTOR=32):
    """
    Convert a WSI slide to a scaled-down PIL image.
    Args:
        slide: An OpenSlide object.
    Returns:
        Tuple consisting of scaled-down PIL image, original width, original height, new width, and new height.
    """
    large_w, large_h = slide.dimensions
    new_w = math.floor(large_w / SCALE_FACTOR)
    new_h = math.floor(large_h / SCALE_FACTOR)
    level = slide.get_best_level_for_downsample(SCALE_FACTOR)
    whole_slide_image = slide.read_region(
        (0, 0), level, slide.level_dimensions[level])
    whole_slide_image = whole_slide_image.convert("RGB")
    img = whole_slide_image.resize((new_w, new_h), Image.Resampling.BILINEAR)
    return img, (large_w, large_h, new_w, new_h)

# main program


def main():
    start = datetime.datetime.now()

    # Open the slide
    slide = openslide.open_slide(args.file)
    # Slide name without extension
    slidename_noext = args.file.split('/')[-1].rsplit('.', 1)[0]
    print(f'[INFO]  Tile extraction starting for slide {slidename_noext}')

    # scale factor
    SCALE = 32
    scaling = slide.dimensions[0]/slide.level_dimensions[args.layer][0]

    # Downscaled version of the slide
    downscaled_img, _ = slide_to_scaled_pil_image(
        slide, SCALE_FACTOR=SCALE)
    draw = ImageDraw.Draw(downscaled_img)

    # Get slide dimensions at layer
    slide_l_w = slide.level_dimensions[args.layer][0]
    slide_l_h = slide.level_dimensions[args.layer][1]

    # Read the mask
    mask = Image.open(args.mask)

    print(f"[INFO]  Input mask size: {mask.size}")
    print(
        f"[INFO]  Input slide size at layer: {str(args.layer)}: ({slide_l_w}, {slide_l_h})")

    # Create output dir
    # output_dir = os.path.dirname(args.file)
    out_dir = os.path.join(args.out, slidename_noext + args.suffix)
    tiles_dir = os.path.join(out_dir, "tiles")
    os.makedirs(tiles_dir, exist_ok=True)

    r_mask_path = os.path.join(
        out_dir,  slidename_noext + '_mask_resized.png')

    try:
        if (not os.path.exists(r_mask_path)):
            print(f"[DEBUG]  Resizing input mask image...")
            # Resize mask to slide dimensions
            r_mask = mask.resize((slide_l_w, slide_l_h))
            if args.save_mask:
                print(f"[DEBUG]  Saving resized input mask image...")
                r_mask.save(r_mask_path)
            r_mask = np.array(r_mask)
        else:
            print(f"[INFO]  Resized input mask found at: {r_mask_path}")
            r_mask = imageio.imread(r_mask_path)
            # r_mask = asarray(r_mask)

        # mask_reshaped = np.transpose(r_mask)

        print(f"[INFO]  Resized mask size: {r_mask.shape}")

        print("[DEBUG]  Tiling slide...")
        # Whole Slide Bag Dataset
        slide_dataset = Whole_Slide_Bag(
            slide, tile_size=args.tile_size, mask=r_mask)
        # Tiles Loader
        tiles_loader = DataLoader(dataset=slide_dataset)
        print(f"[INFO]  Total tiles in slide: {str(len(slide_dataset))}")

        print("[DEBUG]  Applying mask to tiles...")
        count = 0
        for (col, row), res, tile_mask in tiles_loader:
            tissue_indexes = (res[:] > 0.05).nonzero(as_tuple=False)

            for t_idx in list(tissue_indexes):
                count += 1
                coords = np.array([int(col[t_idx]), int(row[t_idx])])

                tile_img = slide.read_region((int(col[t_idx]*scaling), int(
                    row[t_idx]*scaling)), level=args.layer, size=(args.tile_size, args.tile_size))
                tile_img_arr = np.array(tile_img)

                # Apply mask to tile
                masked_tile = cv2.bitwise_and(
                    tile_img_arr, tile_img_arr, mask=np.moveaxis(np.array(tile_mask), 0, -1))

                # Find transparent pixels
                trans_mask = masked_tile[:, :, 3] == 0

                if args.color == 'w':
                    # replace areas of transparency with white and not transparent
                    masked_tile[trans_mask] = [255, 255, 255, 255]
                else:
                    # replace areas of transparency with black and not transparent
                    masked_tile[trans_mask] = [0, 0, 0, 0]

                # Save tile image
                out_tile_img = Image.fromarray(masked_tile)
                out_tile_img.save(os.path.join(
                    tiles_dir, slidename_noext+".X"+str(coords[1])+".Y"+str(coords[0])+".tile.tissue.png"))

                if args.save_thumbnail:
                    s = (int(coords[0]/SCALE * scaling),
                         int(coords[1]/SCALE * scaling))
                    draw.rectangle(((s[0], s[1]), (s[0] + args.tile_size/SCALE * scaling, s[1] +
                                                   args.tile_size/SCALE * scaling)), fill=None, outline="green", width=2)

        print(f"[INFO]  Total tiles in slide with tissue: {str(count)}")

        end = datetime.datetime.now()
        print(
            f'[INFO]  Time required for slide {slidename_noext}: {end - start}')

        if args.save_thumbnail:
            print('[DEBUG]  Saving thumbnail...')
            downscaled_img.save(os.path.join(
                out_dir,  slidename_noext + '_thumb.png'))

        # output_dir = os.path.dirname(args.file)
        # out_dir = os.path.join(output_dir, slidename_noext + args.suffix)
        # os.makedirs(out_dir, exist_ok=True)

        print(f'[INFO]  Tiling performed for slide {slidename_noext}')
    except Exception as e:
        print(f'[ERROR]  Code: {str(e)}')


if __name__ == "__main__":
    main()

# Print the version number
print(f"\n+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}). {COPYRIGHT} +")
print(f"{COPYRIGHT_TEXT}")
# End of file
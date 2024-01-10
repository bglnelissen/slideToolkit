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

parser = argparse.ArgumentParser('extract_tiles')

# Input slide
parser.add_argument('--file', help='path to slide image')

# Input mask
parser.add_argument('--mask', help='path to slide image')

# Out dir
parser.add_argument('--out', default='./', help='path to output directory')

# slide layer to extract tiles
parser.add_argument('--layer', type=int, default=0,
                    help='At which layer to extract tiles')

# size of tiles
parser.add_argument('--tile_size', type=int,
                    default=2000, help='Size of tiles')

# output suffix
parser.add_argument('--suffix', default="",
                    help='Additional output folder suffix')

# output resized mask
parser.add_argument('--save_mask', type=bool, default=False,
                    help='Save resized mask')

# output resized mask
parser.add_argument('--keep_empty', type=bool, default=False,
                    help='Keep emty tiles after masking')

# save thumbnail image
parser.add_argument('--save_thumbnail', type=bool, default=True,
                    help='Keep thumbnail image after masking')

# masking color
parser.add_argument('--color', default="w", help='Masking color (w=white, b=black)')

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

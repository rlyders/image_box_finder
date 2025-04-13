""" Main entry point for the box finder application."""

import argparse
import sys

from .image_utils import process_images

parser = argparse.ArgumentParser(description="Identify boxes in an image.")
parser.add_argument("images", type=str, nargs="+", help="image(s) to be searched for boxes")
parser.add_argument("-o", "--out", dest="out_path",
                    help="output path where processed image(s) will be saved")

args = parser.parse_args()
if len(args.images) == 0:
    print("Error: No images provided.")
    sys.exit(1)

if __name__ == "__main__":
    process_images(args)

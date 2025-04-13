"""Module for file utilities related to image processing."""

import os

from .constants import STEP_NAMES

def get_step_file_name(image_path, out_path, step_num):
    """Returns the file name to be used for the generated image resulting 
    from each step during image processing based on image path, 
    output path, step_num."""
    # filename with extension
    file_name = os.path.basename(image_path)
    file_ext = os.path.splitext(image_path)[1]
    # get base name of file without extension
    image_basename = file_name.replace(file_ext, "")

    out_dir = f'{out_path}/{image_basename}'
    # create out directory
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    return f'{out_dir}/{image_basename}-{step_num}-{STEP_NAMES[step_num]}{file_ext}'

def get_output_path(image_path, output_path):
    """Determine the output path for processed images."""
    if output_path is None:
        # default output path: create a new directory named "out"
        #  within the existing directory of the each given image
        return f"{os.path.dirname(image_path)}/out"
    return output_path

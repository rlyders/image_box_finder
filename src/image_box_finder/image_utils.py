"""Module for processing images in order to identify boxes."""

import os
import cv2
import numpy as np

from .file_utils import get_output_path, get_step_file_name
from .step_image import StepImage

# based on StackOverflow answer by Sreekiran A R: https://stackoverflow.com/a/63085222/9980429

def find_boxes(image_path, out_path):
    """Function to process the image to find boxes and save intermediate steps."""
    if not os.path.isfile(image_path):
        print(f"Error: Given image file not found: {image_path}")
        return

    ### reading input image
    image=cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to read image at {image_path}")
        return
    step_num = 0
    cv2.imwrite(get_step_file_name(image_path, out_path, step_num), image)

    ### Step 1: convert to grayscale
    step_num += 1
    img_gray = convert_to_grayscale(StepImage(image_path, out_path, image), step_num)

    ### Step 2: convert to black and white
    step_num += 1
    img_bw = convert_to_black_and_white(StepImage(image_path, out_path, img_gray), step_num)

    ### common variables for line detection
    line_width = 2
    line_min_width = 15

    ### Step 3: find horizontal lines
    step_num += 1
    img_bw_h = find_horizontal_lines(
        StepImage(image_path, out_path, img_bw),
        line_width, line_min_width, step_num)

    ### Step 4: find vertical lines
    step_num += 1
    img_bw_v = find_vertical_lines(
        StepImage(image_path, out_path, img_bw),
        line_width, line_min_width, step_num)

    ### Step 5: combine horizontal and vertical lines to identify boxes
    step_num += 1
    img_bw_boxes = merge_horizontal_and_vertical_lines(
        StepImage(image_path, out_path, img_bw_h),
          img_bw_v, step_num)

    ### Step 6: highlight boxes using red lining
    step_num += 1
    highlight_boxes(StepImage(image_path, out_path, image), img_bw_boxes, step_num)

def highlight_boxes(img: StepImage, img_bw_boxes, step_num):
    """Function to highlight the identified boxes in the original image"""
    ### get stats on Connected Components
    _, _, stats, _ = cv2.connectedComponentsWithStats(
        ~img_bw_boxes, connectivity=8, ltype=cv2.CV_32S)

    ### drawing recangles for visualisation
    for x,y,w,h,_ in stats[0:]:
        cv2.rectangle(img.image,(x,y),(x+w,y+h),(0,0,255),2)
    cv2.imwrite(get_step_file_name(img.image_path, img.out_path, step_num), img.image)

def force_to_0_or_255(img):
    """Function to convert pixels above 127 to 255 and below to 0."""

    """    Convert the image to binary format where pixels above 127 are set to 255"""
    img[img>127]=255

    """    Convert the image to binary format where pixels below 127 are set to 0"""
    img[img<127]=0
    return img

def merge_horizontal_and_vertical_lines(img: StepImage, img_bw_v, step_num):
    """Function to merge horizontal and vertical lines to form boxes."""
    img_bw_boxes = force_to_0_or_255(force_to_0_or_255(img.image)|force_to_0_or_255(img_bw_v))
    cv2.imwrite(get_step_file_name(img.image_path, img.out_path, step_num), img_bw_boxes)
    return img_bw_boxes

def find_vertical_lines(img: StepImage, line_width, line_min_width, step_num):
    """    Function to find vertical lines in the image."""
    kernal1v = np.ones((line_width,1), np.uint8)
    kernal6v = np.ones((line_min_width,1), np.uint8)
    # bridge small gap in vert lines
    img_bw_v = cv2.morphologyEx(~img.image, cv2.MORPH_CLOSE, kernal1v)
    # kep ony vert lines by eroding everything else in vert direction
    img_bw_v = cv2.morphologyEx(img_bw_v, cv2.MORPH_OPEN, kernal6v)
    cv2.imwrite(get_step_file_name(img.image_path, img.out_path, step_num), img_bw_v)
    return img_bw_v

def find_horizontal_lines(img: StepImage, line_width, line_min_width, step_num):
    """    Function to find horizontal lines in the image."""
    kernal1h = np.ones((1,line_width), np.uint8)
    kernal6h = np.ones((1,line_min_width), np.uint8)

    # bridge small gap in horizonntal lines
    img_bw_h = cv2.morphologyEx(~img.image, cv2.MORPH_CLOSE, kernal1h)
     # kep ony horiz lines by eroding everything else in hor direction
    img_bw_h = cv2.morphologyEx(img_bw_h, cv2.MORPH_OPEN, kernal6h)
    cv2.imwrite(get_step_file_name(img.image_path, img.out_path, step_num), img_bw_h)
    return img_bw_h

def convert_to_black_and_white(img: StepImage, step_num):
    """Convert the grayscale image to black and white using 
    Otsu's thresholding and save the resulting image to a file."""
    _,img_bw = cv2.threshold(img.image,180,225,cv2.THRESH_OTSU)
    cv2.imwrite(get_step_file_name(img.image_path, img.out_path, step_num), img_bw)
    return img_bw

def convert_to_grayscale(img: StepImage, step_num):
    """Convert the image to grayscale and save the 
    resulting image to a file."""
    img_gray=cv2.cvtColor(img.image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(get_step_file_name(img.image_path, img.out_path, step_num), img_gray)
    return img_gray

def process_images(arguments):
    """Process each image to find boxes and save results."""
    for _, img in enumerate(arguments.images):
        out_path = get_output_path(img, arguments.out_path)
        find_boxes(img, out_path)

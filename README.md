# Image Box Finder

## Description

This Python project searches given images for boxes and saves the results to a new image file with the boxes highlighted in red.

CREDITS: This project is based on the following StackOverflow answer by Sreekiran A R: https://stackoverflow.com/a/63085222/9980429

The following steps are taken during the processing of each given image:

 1) convert image to gray scale
 1) convert image to black and white (binary)
 1) identify all horizontal lines
 1) identify all vertical lines
 1) merge horizontal and vertical line to identify boxes
 1) highlight all boxes in red on original source image

After each step in processing, an image showing the results of the step is saved to a new image file with the name suffixed to describe the step # and action taken during each step.

For example, if a source image of `examples/w9-checkboxes-and-signature.tif` is given (and no output directory defined via the "-o" command-line argument), then the images generated during each step in processing will be saved to a file using the following pattern: `examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-{step-num}-{step-desc}.tif`. 

NOTE: The given index (`-0-`...`-6-`) represents the order of processing with `-0-` representing the original, unchanged source image file.

```sh
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-0-orig.tif                 # 0: copy of original source file
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-1-gray.tif                 # step 1: converted to gray scale
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-2-bw.tif                   # step 2: converted to black and white (binary)
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-3-bw_h.tif                 # step 3: found all horizontal lines
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-4-bw_v.tif                 # step 4: found all vertical lines
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-6-bw_boxes.tif             # step 5: merged horizontal and vertical line to identify boxes
examples/out/w9-checkboxes-and-signature/w9-checkboxes-and-signature-7-orig-red-boxes.tif       # step 6: highlighted all boxes in red on original source image
```

## Output directory parameter

If a value is provided for the output directory defined via the "-o" command-line argument, then all generated files will be created in that given directory.

# Example images

The examples directory contains the following files:
 * [form-W9.pdf](examples/form-W9.pdf): this is page 1 of an IRS form W9 downloaded from the IRS website: https://www.irs.gov/pub/irs-pdf/fw9.pdf
 * [w9-checkboxes-and-signature.tif](examples/w9-checkboxes-and-signature.tif): this is a TIFF file that contains just section 3a along with the signature from the IRS form W9
 * [w9-checkboxes-and-signature-signed.tif](examples/w9-checkboxes-and-signature-signed.tif): this is a the same TIFF fo checkboxes and signatures as above, but this one is signed and one of the checkboxes is checked.

# Installation

Starting in the root of this project's directory, run:

```sh
echo "create, install and activate a new Python virtual environment"
pip install virtualenv
virtualenv .venv
source .venv/bin/activate

echo "install packages that this project requires"
pip install -r requirements.txt

echo "install this project as a module named image_box_finder"
pip install .
```

# Usage

Once you have completed installation as noted above in [Installation](#installation), you can run this project.

In the root of this project's directory, run:

```sh
python -m image_box_finder ./examples/w9-checkboxes-and-signature-signed.tif -o out
```

If you want all the generated files to be saved in the same directory as the given source image, then omit the `-o` argument as follows:

```sh
python -m image_box_finder ./examples/w9-checkboxes-and-signature-signed.tif
```

Multiple image files can be provided for processing by simply including the image paths on the command-line separated with spaces as follows:

```sh
python -m image_box_finder ./examples/w9-checkboxes-and-signature-signed.tif ./examples/w9-checkboxes-and-signature.tif
```


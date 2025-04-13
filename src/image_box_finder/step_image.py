""" Module to define a dataclass for step images in image processing."""

from dataclasses import dataclass
import numpy as np

@dataclass
class StepImage:
    """Class to hold information about each step's image processing."""
    image_path: str
    out_path: str
    image: np.ndarray

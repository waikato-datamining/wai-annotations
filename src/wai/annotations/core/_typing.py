"""
Module for types associated with core functionality.
"""
from typing import Tuple

from wai.common.adams.imaging.locateobjects import LocatedObjects

from ._ImageFormat import ImageFormat

# The internal type used as an intermediary for conversions
# Image filename, image data, image format, objects located in image
InternalFormat = Tuple[str, bytes, ImageFormat, LocatedObjects]

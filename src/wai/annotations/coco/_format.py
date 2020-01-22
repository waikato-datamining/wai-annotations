"""
Module defining the COCO external format.
"""
from typing import Tuple, List

from ..core import ImageInfo
from .configuration import Annotation

# Image info, COCO annotations, labels, prefixes
COCOExternalFormat = Tuple[ImageInfo, List[Annotation], List[str], List[str]]

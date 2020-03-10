import os
from typing import Iterator
import csv

from wai.common.cli.options import ClassOption

from ...core import Reader, ImageInfo
from ..utils import get_associated_image_from_filename
from .._format import ROIExternalFormat
from .._ROIObject import ROIObject


class ROIReader(Reader[ROIExternalFormat]):
    """
    Reader of ROI-format CSV files.
    """
    reader_prefix = ClassOption("--prefix", type=str,
                                help="the prefix for output filenames (default = '')")
    reader_suffix = ClassOption("--suffix", type=str,
                                help="the suffix for output filenames (default = '-rois.csv')")

    def read_annotation_file(self, filename: str) -> Iterator[ROIExternalFormat]:
        # Read in the file
        with open(filename, "r") as file:
            # Create a CSV dict reader around the file
            csv_reader = csv.DictReader(file)

            # Extract the contents into dictionaries
            roi_dicts = [dict(row) for row in csv_reader]

        # Get the image filename
        if len(roi_dicts) > 0:
            image_file = roi_dicts[0]["file"]
        else:
            image_file = get_associated_image_from_filename(filename, self.reader_prefix, self.reader_suffix)

        # Get the full path to the image
        image_path = os.path.join(os.path.dirname(filename), image_file)

        # Create the ROI objects from the dictionaries
        roi_objects = list(map(ROIObject.from_dict, roi_dicts))

        yield ImageInfo.from_file(image_path), roi_objects

    def image_info_to_external_format(self, image_info: ImageInfo) -> ROIExternalFormat:
        return image_info, []

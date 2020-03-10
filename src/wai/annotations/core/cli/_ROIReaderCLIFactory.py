"""
Automatically generated by gen-cli.py.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._ClassOption import ClassOption


class ROIReaderCLIFactory(CLIFactory):
    """
    Factory which instantiates the ROIReader class.
    """
    # Options
    input_files = ClassOption('-I', '--input-files', type=str, action='append', help='Files containing lists of input annotation files (can use glob syntax)')
    inputs = ClassOption('-i', '--inputs', type=str, action='append', help='Input annotations files (can use glob syntax)', metavar='files')
    negative_files = ClassOption('-N', '--negative-files', type=str, action='append', help='Files containing lists of negative images (can use glob syntax)')
    negatives = ClassOption('-n', '--negatives', type=str, action='append', help='Image files that have no annotations (can use glob syntax)', metavar='image')
    reader_prefix = ClassOption('--prefix', type=str, help="the prefix for output filenames (default = '')")
    reader_suffix = ClassOption('--suffix', type=str, help="the suffix for output filenames (default = '-rois.csv')")

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.roi.io._ROIReader import ROIReader
        return ROIReader

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()

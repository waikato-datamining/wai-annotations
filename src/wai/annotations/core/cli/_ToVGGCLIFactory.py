"""
Automatically generated by gen-cli.py.
"""
from argparse import Namespace
from typing import Type

from wai.common.cli import CLIFactory, CLIInstantiable
from wai.common.meta.typing import VAR_ARGS_TYPE

from wai.common.cli.options._ClassOption import ClassOption


class ToVGGCLIFactory(CLIFactory):
    """
    Factory which instantiates the ToVGG class.
    """
    # Options
    labels = ClassOption('-l', '--labels', type=str, nargs='+', help='labels to use')
    regex = ClassOption('-r', '--regexp', type=str, help='regular expression for using only a subset of labels', metavar='regexp')

    @classmethod
    def production_class(self, namespace: Namespace) -> Type[CLIInstantiable]:
        from wai.annotations.vgg.convert._ToVGG import ToVGG
        return ToVGG

    @classmethod
    def init_args(self, namespace: Namespace) -> VAR_ARGS_TYPE:
        return (namespace,), dict()

"""
Module which configures the argument parser for the main function.
"""
from argparse import ArgumentParser

# Import the components that are available to us
from ._components import components as available_components

# Create the unconfigured parser
parser: ArgumentParser = ArgumentParser()

# Add any global options
#parser.add_argument(
#    "-v", "--verbose", action="store_true", dest="verbose", required=False,
#    help="whether to be more verbose when generating the records")

parser.add_argument(
    "-c", "--coerce", dest="coerce", required=False, choices=["bbox", "mask"],
    help="whether to coerce located objects into a particular boundary type"
)

# Filter the components into input side...
input_components = {
    name: components[:2]
    for name, components in available_components.items()
    if components[0] is not None and components[1] is not None
}

# ...and output side
output_components = {
    name: components[2:]
    for name, components in available_components.items()
    if components[2] is not None and components[3] is not None
}

# Create a first level sub-parser set for selecting the input type
input_subparsers = parser.add_subparsers(dest="input_type")

# Add each available input type to the parser
for input_type, reader_and_converter in input_components.items():
    # Unpack the reader and converter
    reader, input_converter = reader_and_converter

    # Create a sub-parser for this input type
    input_subparser = input_subparsers.add_parser(input_type)

    # Configure the sub-parser using the components
    reader.configure_parser(input_subparser)
    input_converter.configure_parser(input_subparser)

    # Create a second level sub-parser set for selecting the output type
    output_subparsers = input_subparser.add_subparsers(dest="output_type")

    for output_type, converter_and_writer in output_components.items():
        # Unpack the converter and writer
        writer, output_converter = converter_and_writer

        # Create a sub-parser for this output type
        output_subparser = output_subparsers.add_parser(output_type)

        # Configure the sub-parser using the components
        writer.configure_parser(output_subparser)
        output_converter.configure_parser(output_subparser)

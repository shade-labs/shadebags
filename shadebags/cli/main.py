"""
    CLI definitions for shadebags
    Copyright (C) 2022  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import argparse
import os

import shadebags
from shadebags.defaults import BagDefaults

def get_valid_types():
    return [e.value for e in BagDefaults]

parser = argparse.ArgumentParser(description="Shade compression tool")

subparsers = parser.add_subparsers(help="Different shade options")

compress_parser = subparsers.add_parser('compress', help='Runs the compression algorithm on a bag')
compress_parser.set_defaults(which='compress')
compress_parser.add_argument('file', required=True, help='A path to a bag to compress')
compress_parser.add_argument('type', required=True, help=f'A valid input bag type, valid types are {get_valid_types()}')

decompress_parser = subparsers.add_parser('decompress', help='Decompresses a shadebag into the original or different format')
decompress_parser.set_defaults(which='decompress')
decompress_parser.add_argument('file', required=True, help='A path to a shadebag to decompress')
decompress_parser.add_argument('type', required=True, help=f'A valid input bag type, valid types are {get_valid_types()}')


def main():
    args = vars(parser.parse_args())

    def map_type(input_type: str):
        try:
            return BagDefaults[input_type]
        except KeyError:
            raise KeyError(f"Unable to parse type {input_type} - valid types are {get_valid_types()}")

    try:
        which = args['which']
    except KeyError:
        parser.print_help()
        return

    if which == 'compress':
        if args['path'] is None:
            compress_parser.print_help()

        output_file = f'{os.path.dirname(args["path"])}/{os.path.basename(args["path"]).split(".")[0]}.shade'
        writer = shadebags.Writer(input_file=args['path'], output_file = output_file, bag_type=map_type(args['type']))
        writer.write()


    elif which == 'decompress':
        if args['path'] is None:
            decompress_parser.print_help()

        raise NotImplementedError("Sorry!")


if __name__ == "__main__":
    main()

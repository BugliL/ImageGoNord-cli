import argparse
from pathlib import Path

from argparse import RawDescriptionHelpFormatter

VERSION = (Path(__file__).parent / "VERSION").read_text().strip()
DEFAULT_EXTENSION = ".png"
OUTPUT_IMAGE_NAME = "nord" + DEFAULT_EXTENSION

__doc__ = """ImageGoNord, a converter for a rgb images to norththeme palette.
Usage: gonord [OPTION]...

Mandatory arguments to long options are mandatory for short options too.

Startup:


Theme options:
  --PALETTE[=LIST_COLOR_SET]        the palettes can be found in the
                                    src/palettes/ directory (actually there is
                                    only nord), by replacing 'PALETTE' with a
                                    theme name it is possible to select it. If
                                    necessary you can specify the set of colors
                                    you want to use.
                                    Ex: python src/cli.py --nord=Aurora,PolarNight,SnowStorm
                                    Ex: python src/cli.py --monokai

Email bug reports, questions, discussions to <schrodinger.hat.show@gmail.com>
and/or open issues at https://github.com/Schrodinger-Hat/ImageGoNord/issues/new
"""


def parse_pixels_area(value: str):
    if not value:
        raise TypeError("Invalid value for pixels area: {}".format(value))

    values = value.split(",")
    if len(values) > 2:
        raise ValueError(
            "Invalid number of parameters for pixels area: {}".format(value)
        )

    if not all(map(lambda x: x.isdigit(), values)):
        raise ValueError(
            "Invalid value for pixels area, all should be integer: {}".format(value)
        )

    return values


def get_default_palette_path() -> str:
    return str(Path(__file__).parent / "palettes" / "Nord")


def get_palette_list() -> list[str]:
    return [
        folder.name.lower() for folder in (Path(__file__).parent / "palettes").iterdir()
    ]


def get_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=__doc__,
        add_help=True,
        prog="image-go-nord-client",
        formatter_class=RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=VERSION,
        help="show version number and exit",
    )

    parser.add_argument(
        "-i",
        "--img",
        type=str,
        dest="input_path",
        metavar="PATH",
        required=True,
        help="specify input image path",
    )

    parser.add_argument(
        "-b",
        "--blur",
        action="store_true",
        dest="enable_blur",
        default=False,
        help="use blur on the final result",
    )

    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet_mode",
        default=False,
        help="quiet (no output)",
    )

    parser.add_argument(
        "-o",
        "--out",
        type=str,
        dest="output_path",
        metavar="PATH",
        default=OUTPUT_IMAGE_NAME,
        help="specify output image path",
    )

    parser.add_argument(
        "-na",
        "--no-avg",
        action="store_true",
        dest="disable_avg_pixels",
        default=False,
        help="do not use the average pixels optimization algorithm on conversion",
    )

    parser.add_argument(
        "-pa",
        "--pixels-area",
        type=parse_pixels_area,
        dest="pixels_area",
        metavar="INT[,INT]",
        default=[],
        help="specify pixels of the area for average color calculation",
    )

    return parser

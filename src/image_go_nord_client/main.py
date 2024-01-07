#! /usr/bin/env python3

import logging
import argparse
from pathlib import Path
import sys

from os import listdir
from typing import Union
from ImageGoNord import GoNord
from argparse import RawDescriptionHelpFormatter

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

Conversion:

  -pa=INT,INT, --pixel-area=INT,INT specify pixels of the area for average
                                    color calculation

Email bug reports, questions, discussions to <schrodinger.hat.show@gmail.com>
and/or open issues at https://github.com/Schrodinger-Hat/ImageGoNord/issues/new
"""


class confarg:
    logs = {
        "img": [
            "[INFO] Loading input image: {}",
            "[ERROR] On '{}': you need to pass the image path!",
            "\te.g. --img='Pictures/notNord.jpg'",
        ],
        "out": [
            "[INFO] Set output image name: {}",
            "[ERROR] On '{}': no output filename specify!",
            "\te.g. --out='Pictures/nord.jpg'",
        ],
        "navg": [
            "[INFO] No average pixels selected for algorithm optimization",
            "[ERROR] On '{}': the average pixels do not take any values!",
            "\te.g. --no-average",
        ],
        "pxls": [
            "[INFO] Set up pixels width area: {}",
            "[INFO] Set up pixels height area: {}",
            "[ERROR] On '{}': no value specify within the area pixels!",
            "\te.g. --pixels-area=2 or -pa=-4,-3",
        ],
        "blur": [
            "[INFO] Blur enabled",
            "[ERROR] On '{}': the blur argument do not take any values!",
            "\te.g. --blur",
        ],
        "pals": [
            "[INFO] Use all color set: {}",
            "[INFO] Use palette set: {}",
            "\t {} \u2713",
            "\t {} \u2718",
            "[WARNING] No theme specified, use default Nord theme",
            "[WARNING] No set found for: {} \u2753",
        ],
        "err": ["[INFO] No image created, solve all ERROR and retry."],
    }


VERSION = (Path(__file__).parent / "VERSION").read_text().strip()
DEFAULT_EXTENSION = ".png"
OUTPUT_IMAGE_NAME = "nord" + DEFAULT_EXTENSION

__ALL__ = ["to_console", "get_version", "main"]


def to_console(quiet_mode, *params):
    if quiet_mode:
        return

    for param in params:
        print(param)

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

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
    "-o",
    "--out",
    type=str,
    dest="output_path",
    metavar="PATH",
    default=OUTPUT_IMAGE_NAME,
    help="specify output image path",
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
    "-na",
    "--no-avg",
    action="store_true",
    dest="disable_avg_pixels",
    default=False,
    help="do not use the average pixels optimization algorithm on conversion",
)

parser.add_argument(
    "-b",
    "--blur",
    action="store_true",
    dest="enable_blur",
    default=False,
    help="use blur on the final result",
)

def main(argv: Union[list[str], None] = None):
    global OUTPUT_IMAGE_NAME

    output_image_path = OUTPUT_IMAGE_NAME
    PALETTE_CHANGED = False

    if argv is None:
        argv = sys.argv.copy()

    arguments, _ = parser.parse_known_args(argv.copy())
    args = argv[1:]
    if not argv:
        parser.print_help()
        return 1

    if not arguments.input_path:
        parser.print_help()
        return 1

    if arguments.quiet_mode:
        logging.basicConfig(level=logging.CRITICAL)

    go_nord = GoNord()

    # Get absolute path of source project
    src_path = Path(__file__).parent

    # Get all palettes created
    palettes = [folder.name.lower() for folder in (src_path / "palettes").iterdir()]
    # palettes = [palette.lower() for palette in listdir(src_path + "/palettes")]

    image = go_nord.open_image(arguments.input_path)
    logging.info("Loading input image: %s", arguments.input_path)

    output_image_path = arguments.output_path
    logging.info("Set output image name: %s", output_image_path)

    if arguments.enable_blur:
        go_nord.enable_gaussian_blur()
        logging.info("Blur enabled")
        
    if arguments.disable_avg_pixels:
        go_nord.disable_avg_algorithm()
        logging.info("No average pixels selected for algorithm optimization")

    for arg in args:
        key_value = [kv for kv in arg.split("=", 1) if kv != ""]
        key = key_value[0].lower()

        condition_argument = key in ["-pa", "--pixels-area"]
        if condition_argument:
            try:
                area_value = key_value[1].split(",")
                try:
                    go_nord.set_avg_box_data(w=area_value[0], h=area_value[1])
                    to_console(
                        arguments.quiet_mode,
                        confarg.logs["pxls"][0].format(area_value[0]),
                        confarg.logs["pxls"][1].format(area_value[1]),
                    )
                except IndexError:
                    go_nord.set_avg_box_data(w=area_value[0], h=area_value[0])
                    to_console(
                        arguments.quiet_mode,
                        confarg.logs["pxls"][0].format(area_value[0]),
                        confarg.logs["pxls"][1].format(area_value[0]),
                    )
            except IndexError:
                to_console(
                    arguments.quiet_mode,
                    confarg.logs["pxls"][-2].format(arg),
                    confarg.logs["pxls"][-1],
                    confarg.logs["err"][0],
                )
                return 1

        for palette in palettes:
            if "--{}".format(palette) in key:
                palette_path = src_path / "palettes" / palette.capitalize()
                go_nord.set_palette_lookup_path(str(palette_path) + "/")
                if len(key_value) > 1:
                    go_nord.reset_palette()
                    palette_set = [
                        palette_file.replace(".txt", "")
                        for palette_file in listdir(palette_path)
                    ]
                    selected_colors = [
                        selected_color.lower()
                        for selected_color in key_value[1].split(",")
                    ]
                    to_console(
                        arguments.quiet_mode,
                        confarg.logs["pals"][1].format(palette.capitalize()),
                    )
                    for selected_color in selected_colors:
                        lowered_palette = list(map(str.lower, palette_set))
                        if selected_color in lowered_palette:
                            index_color = lowered_palette.index(selected_color)
                            go_nord.add_file_to_palette(
                                palette_set[index_color] + ".txt"
                            )
                            to_console(
                                arguments.quiet_mode,
                                confarg.logs["pals"][2].format(
                                    palette_set[index_color]
                                ),
                            )
                            PALETTE_CHANGED = True
                        else:
                            to_console(
                                arguments.quiet_mode,
                                confarg.logs["pals"][-1].format(selected_color),
                            )
                    for palette_color in palette_set:
                        if palette_color.lower() not in selected_colors:
                            to_console(
                                arguments.quiet_mode,
                                confarg.logs["pals"][3].format(palette_color),
                            )
                else:
                    PALETTE_CHANGED = True
                    to_console(
                        arguments.quiet_mode,
                        confarg.logs["pals"][0].format(palette.capitalize()),
                    )
                    palette_path = src_path / "palettes" / palette.capitalize()
                    go_nord.reset_palette()
                    palette_set = [
                        palette_file.replace(".txt", "")
                        for palette_file in listdir(palette_path)
                    ]
                    go_nord.set_palette_lookup_path(str(palette_path) + "/")
                    for palette_color in palette_set:
                        go_nord.add_file_to_palette(palette_color + ".txt")

    if not PALETTE_CHANGED:
        to_console(arguments.quiet_mode, confarg.logs["pals"][4])
        palette_path = src_path / "palettes" / "Nord"
        go_nord.reset_palette()
        palette_set = [
            palette_file.name.replace(".txt", "")
            for palette_file in palette_path.iterdir()
        ]
        go_nord.set_palette_lookup_path(str(palette_path) + "/")
        for palette_color in palette_set:
            go_nord.add_file_to_palette(palette_color + ".txt")

    go_nord.convert_image(image, save_path=output_image_path)

    return 0

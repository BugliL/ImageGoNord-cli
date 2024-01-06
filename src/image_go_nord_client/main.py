#! /usr/bin/env python3
"""ImageGoNord, a converter for a rgb images to norththeme palette.
Usage: gonord [OPTION]...

Mandatory arguments to long options are mandatory for short options too.

Startup:
  -h,  --help                       print this help and exit

  -v,  --version                    display the version of Image Go Nord and
                                    exit

Logging:
  -q,  --quiet                      quiet (no output)

I/O Images:
  -i=FILE,  --img=FILE              specify input image name

  -o=FILE,  --out=FILE              specify output image name

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

  -na, --no-avg                     do not use the average pixels optimization
                                    algorithm on conversion

  -pa=INT,INT, --pixel-area=INT,INT specify pixels of the area for average
                                    color calculation

  -b, --blur                        use blur on the final result


Email bug reports, questions, discussions to <schrodinger.hat.show@gmail.com>
and/or open issues at https://github.com/Schrodinger-Hat/ImageGoNord/issues/new
"""

import sys
import re
from os import path, listdir
from typing import Union
from ImageGoNord import GoNord

class confarg:
    logs = {

    "img": [
        "[INFO] Loading input image: {}",
        "[ERROR] On '{}': you need to pass the image path!",
        "\te.g. --img='Pictures/notNord.jpg'"
    ],

    "out": [
        "[INFO] Set output image name: {}",
        "[ERROR] On '{}': no output filename specify!",
        "\te.g. --out='Pictures/nord.jpg'"
    ],

    "navg": [
        "[INFO] No average pixels selected for algorithm optimization",
        "[ERROR] On '{}': the average pixels do not take any values!",
        "\te.g. --no-average"
    ],

    "pxls": [
        "[INFO] Set up pixels width area: {}",
        "[INFO] Set up pixels height area: {}",
        "[ERROR] On '{}': no value specify within the area pixels!",
        "\te.g. --pixels-area=2 or -pa=-4,-3"
    ],

    "blur": [
        "[INFO] Blur enabled",
        "[ERROR] On '{}': the blur argument do not take any values!",
        "\te.g. --blur"
    ],

    "pals": [
        "[INFO] Use all color set: {}",
        "[INFO] Use palette set: {}",
        "\t {} \u2713",
        "\t {} \u2718",
        "[WARNING] No theme specified, use default Nord theme",
        "[WARNING] No set found for: {} \u2753",
    ],

    "err": [
        "[INFO] No image created, solve all ERROR and retry."
    ]

}


VERSION = open(path.dirname(path.realpath(__file__)) + "/VERSION", 'r').readline()
DEFAULT_EXTENSION = ".png"
QUIET_MODE = False
OUTPUT_IMAGE_NAME = "nord" + DEFAULT_EXTENSION
PALETTE_CHANGED = False

__ALL__ = ["to_console", "get_version", "main"]

def to_console(*params):
    """<Short Description>

      <Description>

    Parameters
    ----------
    <argument name>: <type>
      <argument description>
    <argument>: <type>
      <argument description>

    Returns
    -------
    <type>
      <description>
    """
    if QUIET_MODE:
        return
    for param in params:
        print(param)


def get_version():
    """<Short Description>

      <Description>

    Parameters
    ----------
    <argument name>: <type>
      <argument description>
    <argument>: <type>
      <argument description>

    Returns
    -------
    <type>
      <description>
    """
    file_version = open(path.dirname(path.realpath(__file__)) + "/VERSION")
    return file_version.readline()

def main(argv: Union[list[str] , None] = None):
    global OUTPUT_IMAGE_NAME
    global PALETTE_CHANGED
    global QUIET_MODE

    output_image_name = OUTPUT_IMAGE_NAME

    if argv is None:
        argv = sys.argv.copy()
    
    args = argv[1:]

    if len(args) == 0:
        print(__doc__)
        return 1

    # If help given then print the docstring of the module and exit
    if "--help" in args or "-h" in args:
        print(__doc__)
        return 0

    if "--version" in args or "-v" in args:
        print(VERSION)
        return 0

    go_nord = GoNord()

    IMAGE_ARGUMENT_PATTERN = r'-(-img|i)=*'
    IS_IMAGE_PASSED = False
    for arg in args:
        searched_arg = re.search(IMAGE_ARGUMENT_PATTERN, arg)
        if searched_arg is not None:
            IS_IMAGE_PASSED = True
            break
    if not IS_IMAGE_PASSED:
        to_console(confarg.logs["img"][1].format(arg),
                   confarg.logs["img"][-1],
                   confarg.logs["err"][0])
        return 1

    QUIET_MODE = "-q" in args or "--quiet" in args

    # Get absolute path of source project
    src_path = path.dirname(path.realpath(__file__))

    # Get all palettes created
    palettes = [palette.lower() for palette in listdir(src_path + "/palettes")]

    for arg in args:

        key_value = [kv for kv in arg.split("=", 1) if kv != ""]
        key = key_value[0].lower()

        condition_argument = key in ["--img", "-i"]
        IMAGE_PATTERN = r'([A-z]|[\/|\.|\-|\_|\s])*\.([a-z]{3}|[a-z]{4})$'
        if condition_argument:
            if (len(key_value) > 1 and
                re.search(IMAGE_PATTERN, key_value[1]) is not None):
                image = go_nord.open_image(key_value[1])
                to_console(confarg.logs["img"][0].format(
                    src_path + "/" + key_value[1]))
            else:
                to_console(confarg.logs["img"][1].format(arg),
                           confarg.logs["img"][-1],
                           confarg.logs["err"][0])
                return 1
            continue

        condition_argument = key in ["--out", "-o"]
        if condition_argument:
            if len(key_value) > 1:
                output_image_name = key_value[1]
                # If the image name have already an extension do not set the
                # default one
                output_image_name += "" if re.search(
                    IMAGE_PATTERN, output_image_name) else DEFAULT_EXTENSION
                to_console(confarg.logs["out"][0].format(
                    src_path + "/" + output_image_name))
            else:
                to_console(confarg.logs["out"][1].format(arg),
                           confarg.logs["out"][-1],
                           confarg.logs["err"][0])
                return 1
            continue

        condition_argument = key in ["--no-avg", "-na", "--no-avg-pixels"]
        if condition_argument:
            if len(key_value) > 1:
                to_console(confarg.logs["navg"][1].format(arg),
                           confarg.logs["navg"][-1],
                           confarg.logs["err"][0])
                return 1
            else:
                go_nord.disable_avg_algorithm()
                to_console(confarg.logs["navg"][0])
            continue

        condition_argument = key in ["-pa", "--pixels-area"]
        if condition_argument:
            try:
                area_value = key_value[1].split(",")
                try:
                    go_nord.set_avg_box_data(w=area_value[0], h=area_value[1])
                    to_console(confarg.logs["pxls"][0].format(area_value[0]),
                               confarg.logs["pxls"][1].format(area_value[1]))
                except IndexError:
                    go_nord.set_avg_box_data(w=area_value[0], h=area_value[0])
                    to_console(confarg.logs["pxls"][0].format(area_value[0]),
                               confarg.logs["pxls"][1].format(area_value[0]))
            except IndexError:
                to_console(confarg.logs["pxls"][-2].format(arg),
                           confarg.logs["pxls"][-1],
                           confarg.logs["err"][0])
                return 1

        condition_argument = key in ["--blur", "-b"]
        if condition_argument:
            if len(key_value) > 1:
                to_console(confarg.logs["blur"][-2].format(arg),
                           confarg.logs["blur"][-1],
                           confarg.logs["err"][0])
                return 1
            else:
                go_nord.enable_gaussian_blur()
                to_console(confarg.logs["blur"][0])
            continue
        del condition_argument

        for palette in palettes:
            if "--{}".format(palette) in key:
                palette_path = src_path + "/palettes/" + palette.capitalize() + "/"
                go_nord.set_palette_lookup_path(palette_path)
                if len(key_value) > 1:
                    go_nord.reset_palette()
                    palette_set = [palette_file.replace(".txt", '')
                                   for palette_file in listdir(palette_path)]
                    selected_colors = [selected_color.lower() for selected_color in key_value[1].split(",")]
                    to_console(confarg.logs["pals"][1]
                               .format(palette.capitalize()))
                    for selected_color in selected_colors:
                        lowered_palette = list(map(str.lower, palette_set))
                        if selected_color in lowered_palette:
                            index_color = lowered_palette.index(selected_color)
                            go_nord.add_file_to_palette(
                                palette_set[index_color] + ".txt")
                            to_console(confarg.logs["pals"][2]
                                       .format(palette_set[index_color]))
                            PALETTE_CHANGED = True
                        else:
                            to_console(confarg.logs["pals"][-1]
                                       .format(selected_color))
                    for palette_color in palette_set:
                        if palette_color.lower() not in selected_colors:
                            to_console(confarg.logs["pals"][3]
                                       .format(palette_color))
                else:
                    PALETTE_CHANGED = True
                    to_console(confarg.logs["pals"][0]
                               .format(palette.capitalize()))
                    palette_path = src_path + "/palettes/" + palette.capitalize() + "/"
                    go_nord.reset_palette()
                    palette_set = [palette_file.replace(".txt", '')
                                   for palette_file in listdir(palette_path)]
                    go_nord.set_palette_lookup_path(palette_path)
                    for palette_color in palette_set:
                        go_nord.add_file_to_palette(
                            palette_color + ".txt")

    if not PALETTE_CHANGED:
        to_console(confarg.logs["pals"][4])
        palette_path = src_path + "/palettes/Nord/"
        go_nord.reset_palette()
        palette_set = [palette_file.replace(".txt", '')
                       for palette_file in listdir(palette_path)]
        go_nord.set_palette_lookup_path(palette_path)
        for palette_color in palette_set:
            go_nord.add_file_to_palette(
                palette_color + ".txt")

    quantize_image = go_nord.convert_image(
        image,
        save_path=output_image_name)

    return 0
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: Package Main
Author: K4YT3X
Date Created: September 15, 2022
Last Modified: September 15, 2022
"""

import argparse
import sys
from pathlib import Path

from loguru import logger

from . import __version__
from .sds_submaker import LOGURU_FORMAT, SdsSubMaker


def parse_arguments() -> argparse.Namespace:
    """
    parse command line arguments

    :rtype argparse.Namespace: command parsing results
    """
    parser = argparse.ArgumentParser(
        prog="sds-submaker",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=Path,
        help="path to the directory that contains the recordings",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output subtitle file path",
        required=True,
    )
    parser.add_argument(
        "-f",
        "--fontname",
        help="subtitle font name (mono font recommended)",
        default="Iosevka Fixed",
    )
    parser.add_argument(
        "-s", "--fontsize", type=int, help="subtitle font size", default=20
    )
    parser.add_argument(
        "-a",
        "--alignment",
        type=int,
        help="subtitle alignment (ASS specification integer)",
        default=4,
    )
    return parser.parse_args()


def main() -> int:
    """
    command line entrypoint for direct CLI invocation

    :rtype int: 0 if completed successfully, else other int
    """

    try:
        # parse command line arguments
        args = parse_arguments()

        # check input/output file paths
        if not args.input.exists():
            logger.critical(f"Cannot find input directory: {args.input}")
            return 1
        if not args.input.is_dir():
            logger.critical("Input path is not a directory")
            return 1
        if not args.output.parent.exists():
            logger.critical(f"Output directory does not exist: {args.output.parent}")
            return 1

        # remove default handler
        logger.remove()

        # add new sink with custom handler
        logger.add(sys.stderr, colorize=True, format=LOGURU_FORMAT)

        # print package version and copyright notice
        logger.opt(colors=True).info(f"<magenta>SDS SubMaker {__version__}</magenta>")
        logger.opt(colors=True).info("<magenta>Copyright (C) 2022 K4YT3X.</magenta>")

        SdsSubMaker.generate_subtitle(
            args.input,
            args.output,
            {
                "fontname": args.fontname,
                "fontsize": args.fontsize,
                "alignment": args.alignment,
            },
        )

    # don't print the traceback for manual terminations
    except KeyboardInterrupt:
        return 2

    except Exception as error:
        logger.exception(error)
        return 1

    # if no exceptions were produced
    else:
        logger.success("Processing completed successfully")
        return 0


if __name__ == "__main__":
    sys.exit(main())

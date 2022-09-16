#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: SDS Subtitle Maker
Author: K4YT3X
Date Created: September 15, 2022
Last Modified: September 15, 2022
"""
from pathlib import Path

import ffmpeg
import pysubs2
from dateutil import parser

SUB_TEMPLATE = """\
System:     {system}\\N\
Division:   {division}\\N\
Talkgroup:  {talkgroup}\\N\
Unit:       {unit}\\N\
Time:       {time}
"""

# format string for Loguru loggers
LOGURU_FORMAT = (
    "<green>{time:HH:mm:ss.SSSSSS!UTC}</green> | "
    "<level>{level: <8}</level> | "
    "<level>{message}</level>"
)


class SdsSubMaker:
    @staticmethod
    def generate_subtitle(
        input_directory_path: Path, output_subtitle_path: Path, style: dict
    ) -> None:

        subtitle_file = pysubs2.SSAFile()
        subtitle_file.styles["Default"] = pysubs2.SSAStyle(**style)

        elapsed_time = 0

        for index, recording in enumerate(
            sorted(
                [p for p in Path(input_directory_path).iterdir() if p.suffix == ".wav"]
            )
        ):

            # retrieve audio file metadata
            metadata = ffmpeg.probe(recording)
            duration = float(metadata["format"]["duration"])
            tags = metadata["format"]["tags"]

            # generate subtitle for the file
            subtitle_file.insert(
                index,
                pysubs2.SSAEvent(
                    start=elapsed_time,
                    end=pysubs2.make_time(s=duration),
                    text=SUB_TEMPLATE.format(
                        system=tags.get("artist"),
                        division=tags.get("genre"),
                        talkgroup=tags.get("title"),
                        unit=tags.get("encoded_by"),
                        time=parser.parse(tags.get("date")).strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    ),
                ),
            )

            elapsed_time += pysubs2.make_time(s=duration)
        subtitle_file.save(output_subtitle_path)

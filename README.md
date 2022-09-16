# SDS SubMaker

This simple Python script generates subtitles from metadata in SDS100/SDS200 recordings. This makes it easier for the recordings to be made into videos.

## Example

![image](https://user-images.githubusercontent.com/21986859/190550460-3382ff88-f49d-4b5f-ade8-10e8664d573c.png)

## Installation

I'll assume you have basic Linux and Git knowledge.

```shell
# clone the repository
git clone https://github.com/k4yt3x/sds-submaker.git

# enter the directory
cd sds-submaker

# install the script with pip
pip install .
```

## Quick Start

You will need to copy all of your SDS recording `.wav` files into a directory. The directory will look something like:

```shell
$ ls -1 test
2022-09-12_16-05-35.wav
2022-09-12_16-05-50.wav
2022-09-12_16-06-08.wav
2022-09-12_16-06-30.wav
2022-09-12_17-16-35.wav
2022-09-12_17-17-06.wav
2022-09-12_17-17-17.wav
```

Then, run SDS SubMaker with `--input` set to the path to that directory and `--output` set to where you want the generated subtitle file to be placed. Note that while the file name can have a suffix of `.ass`, `.srt`, or any other extension which the `pysubs2` library supports, setting them to anything other than `.ass` will result in the loss of the subtitle format (i.e., font, format, etc.).

Because ASS doesn't have the tabular character `\t` or I don't know how to use it, spaces are used to align the texts. Therefore, it is recommended to use a mono font, otherwise the texts will be out of alignment. The default font is set to `Iosevka Fixed`, and you can, of course, change it and the font size. Run the program with `-h` for more information.

```shell
sds-submaker -i test -o test.ass
```

This is where we leave the scope of this script and use FFmpeg and ImageMagick to finsh the rest of the steps. First, we use need to concatenate all audio files into a single file:

```shell
# enter the directory
cd test

# produce a list of files that need to be merged
ls -1 *.wav | sed -e 's/^/file /' > list.txt

# use FFmepg to merge all of the audio files into merged.wav
ffmpeg -f concat -safe 0 -i list.txt -c copy merged.wav
```

Then we can generate a video with a black background from the audio file.

```shell
convert -size 1920x1080 xc:black jpeg:- | ffmpeg -y -f image2pipe -i - -i merged.wav -filter_complex "loop=-1:1:0" -shortest merged.mp4
```

Finally, we burn the subtitle into the video.

```shell
ffmpeg -i merged.mp4 -vf subtitles=test.ass -c:a copy final.mp4
```

# pyCvExtractAvgColor
A python script to select a region of interest in a video and
extract the average color of that region as a time series.
A csv file with columns for (R)ed, (G)reen and (B)lue color values
as well as a png graphic with the color value over time is saved.

There is also a script to call ffmpeg and extract the right audio channel of
the video in case an acoustic trigger signal was inserted.

### Installation
Replace environmentName with anything you like.
```
conda create -n environtmentName python=3
conda activate environmentName
pip install -r requirements.txt
```

### Usage (video)
```
usage: pyCvExtractAvgColor.py [-h] -v VIDEO [-a AREA] [-s SPEED]

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        Path to input video file
  -a AREA, --area AREA  Area (x1, y1, x2, y2) of the ROI in the video
  -s SPEED, --speed SPEED
                        Manual video frame search speed
```

---
__Example 1:__ This will load the video input.mp4 and play the video
frame by frame until you selected a region of interest.
Press 's' and select an area with your mouse.
Confirm the area by pressing the return or space key.
It will print the coordinates of the selected region before starting to
extract the average color of that area.
```
python pyCvExtractAvgColor.py -v input.mp4
```

---
__Example 2:__ This will load every 30th frame of the video input.mp4 and show them
frame by frame until you selected a region of interest.
Press 's' and select an area with your mouse.
Confirm the area by pressing the return or space key.
It will print the coordinates of the selected region before starting to
extract the average color of that area.
```
python pyCvExtractAvgColor.py -v input.mp4 -s 30
```

---
__Example 3:__ This will load the video input.mp and extract the average color of the area
that was specified as input argument.
```
python pyCvExtractAvgColor.py -v input.mp4 -a x1,y1,x2,y2
```
or
```
python pyCvExtractAvgColor.py -v input.mp4 -a "x1, y1, x2, y2"
```

### Usage (audio)
```
usage: extractAudioTrigger.py [-h] -v VIDEO [-e EXT] [-ao AUDIOOUT] [-o OUT]

optional arguments:
  -h, --help            show this help message and exit
  -v VIDEO, --video VIDEO
                        Input video file
  -e EXT, --ext EXT     Video file extension
  -ao AUDIOOUT, --audioout AUDIOOUT
                        Output path for audio file
  -o OUT, --out OUT     Output path for audio trigger file
```

---
__Example:__ This will load the video input.mp4 and call ffmpeg to extract the
right audio channel. If a path is given instead of a file, all files with the
file extension specified by ```--ext``` (default: MP4) will be processed.
The audio channel is saved as wav file in the current working directory or to a
path that can be specified with ```--audioout```. Next, the audio is loaded and
peaks due to non-linearities will be extracted. The threshold is hardcoded and
set to mean+10*std. A csv file with duration of the audio input is saved with
the trigger state (0 - off, 1 - on) and the time. The output folder can be
specified with ```--out```.

```
# batch processing of all files with .MP4 extension
python pyCvExtractAvgColor.py -v video_folder
```

```
# batch processing of all files with the fiven extension
python pyCvExtractAvgColor.py -v video_folder -e MOV
```

```
# Processing of input.mp4. All outputs will be in the current working directory
python pyCvExtractAvgColor.py -v input.mp4
```

```
# Processing of input.mp4. Audio output will be saved to the audio_out folder.
# Triggers will be saved to the audio_trigger folder.
python pyCvExtractAvgColor.py -v input.mp4 -ao audio_out -o audio_trigger
```

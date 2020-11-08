# pyCvExtractAvgColor
A python script to select a region of interest in a video and
extract the average color of that region as a time series.
A csv file with columns for (R)ed, (G)reen and (B)lue color values
as well as a png graphic with the color value over time is saved.

### Installation
Replace environmentName with anything you like.
```
conda create -n environtmentName python=3
conda activate environmentName
pip install -r requirements.txt
```

### Usage
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

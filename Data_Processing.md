# Reencode (but probably actually just change containers) from AVI to MP4
```ffmpeg -i in.avi out.mp4```
# Split an MP4 Video
```ffmpeg -i in.mp4 -filter:v "crop=<CROP_WIDTH>:<CROP_HEIGHT>:<START_X>:<START_Y>" out.mp4```

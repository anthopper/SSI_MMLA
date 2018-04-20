# Split an avi file
```ffmpeg -i in.avi -filter:v "crop=<CROP_WIDTH>:<CROP_HEIGHT>:<START_X>:<START_Y>" out.avi```

# Reencode (but probably actually just change containers) from AVI to MP4
```ffmpeg -i in.avi out.mp4```

Note: (X,Y) coordinates are using top-left origin 

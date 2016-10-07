#!/bin/bash

# Scropt converts avi to mp4

BASE_DIR="/home/weather/sec_video"

for f in ${BASE_DIR}/*.avi; do
    # Strip out the path
    filename="${f##*/}"
    base="${filename%.*}"
    ext="${filename##*.}"

    target="${BASE_DIR}/${base}.mp4"

    # Convert it if it does not already exist
    if [ ! -f ${target} ]; then
        ffmpeg -i ${f} -c:v libx264 -c:a libfaac -movflags +faststart ${target}
    fi
done

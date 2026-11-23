#!/bin/bash
# Usage: bash composite.sh out.mp4 S1Intro S2DeBai S3Buoc1 S4Giai S5Ket
# Concats the 1080x1920 Manim scenes, puts the matted teacher (teacher_rgba.mov) bottom-right,
# voice from cut_crop.mov, loudnorm -14 LUFS.
set -e
OUT=$1; shift
V=media/videos/scenes/1920p30
: > scenes_list.txt
for sc in "$@"; do echo "file '$V/$sc.mp4'" >> scenes_list.txt; done
ffmpeg -hide_banner -loglevel error -y -f concat -safe 0 -i scenes_list.txt -i teacher_rgba.mov -i cut_crop.mov \
  -filter_complex "[0:v]fps=30,setpts=PTS-STARTPTS[bg];[1:v]scale=506:-1:flags=lanczos,format=rgba[tc];[bg][tc]overlay=x=W-w:y=H-h:shortest=1:format=auto,format=yuv420p[v];[2:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 18 -profile:v high -r 30 -c:a aac -b:a 192k -movflags +faststart -shortest "$OUT"

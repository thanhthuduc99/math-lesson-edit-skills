#!/bin/bash
# Usage: bash mux.sh cut.mp4 out.mp4 Card1=3.4 Card2=43.9 Card3=71.6 Card4=114.6
# Overlays transparent card .mov files (manim -t --format=mov) on the live video at their T0 (cut seconds).
# Audio: original voice, loudnorm -14 LUFS. No music.
set -e
SRC=$1; OUT=$2; shift 2
V=media/videos/cards/1080p30
IN=(-i "$SRC"); FC="[0:v]fps=30,format=yuv420p,setsar=1[b0];"
i=0
for kv in "$@"; do
  k=${kv%%=*}; t=${kv#*=}; i=$((i+1))
  IN+=(-i "$V/$k.mov")
  FC+="[$i:v]setpts=PTS-STARTPTS+$t/TB[o$i];[b$((i-1))][o$i]overlay=eof_action=pass[b$i];"
done
FC+="[b$i]format=yuv420p[v];[0:a]loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[a]"
ffmpeg -hide_banner -loglevel error -y "${IN[@]}" -filter_complex "$FC" \
  -map "[v]" -map "[a]" -r 30 -c:v libx264 -preset medium -crf 18 -profile:v high -pix_fmt yuv420p \
  -c:a aac -b:a 192k -movflags +faststart "$OUT"

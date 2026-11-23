# Usage: python make_crop.py seg.mp4 X Y [W=440 H=340]
# Cuts seg.mp4 by cuts.json and crops the webcam box (top-left X,Y in 1920x1080) -> cut_crop.mov (+ voice).
# Frame-exact video trims, sample-exact audio trims (48 kHz), 12 ms fades at every join.
import json, subprocess, sys

src, X, Y = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
W = int(sys.argv[4]) if len(sys.argv) > 4 else 440
H = int(sys.argv[5]) if len(sys.argv) > 5 else 340
segs = json.load(open("cuts.json"))["segments"]
fc = []
for i, s in enumerate(segs):
    a, b = s["src"]
    fa, fb = round(a * 30), round(b * 30)
    sa, sb = round(a * 48000), round(b * 48000)
    d = (sb - sa) / 48000
    fc.append(f"[0:v]trim=start_frame={fa}:end_frame={fb},setpts=PTS-STARTPTS,crop={W}:{H}:{X}:{Y}[v{i}];")
    fc.append(f"[0:a]atrim=start_sample={sa}:end_sample={sb},asetpts=PTS-STARTPTS,"
              f"afade=t=in:d=0.012,afade=t=out:st={d - 0.012:.4f}:d=0.012[a{i}];")
fc.append("".join(f"[v{i}][a{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=1[vo][ao]")
open("cut_filter.txt", "w").write("\n".join(fc))
subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-filter_complex_script", "cut_filter.txt",
                "-map", "[vo]", "-map", "[ao]", "-r", "30", "-c:v", "libx264", "-crf", "12", "-preset", "veryfast",
                "-c:a", "pcm_s16le", "cut_crop.mov"], check=True)
print("cut_crop.mov", len(segs), "segments")

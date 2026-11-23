# Usage: python inkmap.py cut.mp4 cues.json out_dir
# For each question window: per-pixel MIN over 1 fps frames = every stroke the teacher ever draws.
# Areas still clean in the ink map are safe spots for a card. Also prints scroll points (big frame diffs).
import sys, os, json, subprocess, numpy as np
from PIL import Image

video, cues, out = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
os.makedirs(out, exist_ok=True)
W, H = 960, 540


def frame(t):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", video, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    return np.frombuffer(r.stdout, np.uint8).reshape(H, W, 3)


for k, c in cues.items():
    ts = np.arange(c["start"], c["end"], 1.0)
    fs = [frame(t) for t in ts]
    d = [float(np.abs(fs[i + 1].astype(int) - fs[i].astype(int)).mean()) for i in range(len(fs) - 1)]
    print(k, "scroll/jump at:", [round(ts[i + 1], 1) for i, v in enumerate(d) if v > 6])
    Image.fromarray(np.min(np.stack(fs), axis=0)).save(f"{out}/ink_{k}.jpg", quality=85)

# Usage: python cutlist.py keep.json seg.wav tx.json
# keep.json: [[14.16, 18.98], [19.70, 22.16], ...]  source seconds of seg.mp4, picked by reading tx.txt
# Splits each kept range at pauses > 0.4 s (keeps 0.12 s pad), snaps to 30 fps.
# Output: cuts.json {segments:[{src:[a,b], out:[x,y]}], total}, words_out.json (word times in output seconds).
import json, re, subprocess, sys

KEEP = json.load(open(sys.argv[1]))
sil = subprocess.run(["ffmpeg", "-hide_banner", "-i", sys.argv[2], "-af", "silencedetect=noise=-38dB:d=0.4",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
SIL = list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", sil)],
               [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sil)]))
words = sorted(w for s in json.load(open(sys.argv[3], encoding="utf-8")) for w in s["w"])
PAD = 0.12
segs = []
for a, b in KEEP:
    cur = a
    for s, e in SIL:
        if s > a and e < b and e - s > 0.4:
            segs.append((cur, s + PAD))
            cur = e - PAD
    segs.append((cur, b))
segs = [(round(x * 30) / 30, round(y * 30) / 30) for x, y in segs if y - x > 0.05]
out, t, owords = [], 0.0, []
for x, y in segs:
    out.append({"src": [x, y], "out": [round(t, 3), round(t + y - x, 3)]})
    for w in words:
        if w[0] >= x - 0.02 and w[1] <= y + 0.02:
            owords.append([round(w[0] - x + t, 3), round(w[1] - x + t, 3), w[2].strip(), w[0]])
    t += y - x
json.dump({"segments": out, "total": round(t, 3)}, open("cuts.json", "w", encoding="utf-8"), indent=1)
json.dump(owords, open("words_out.json", "w", encoding="utf-8"), ensure_ascii=False)
print("segments", len(out), "total", round(t, 2))

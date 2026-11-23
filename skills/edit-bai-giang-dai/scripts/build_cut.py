# Usage: python build_cut.py plan.json [--render]
# plan.json:
# {
#   "src": "src.mp4", "audio": "audio16k.wav",
#   "keep": {"c1": [[33.55, 66.8], [69.3, 73.62]], "c2": [[74.8, 85.2]]},   # source seconds, per question
#   "cues": {"c1": {"y0": 49.67, "pick": 70.62}}                            # cue words, source seconds
# }
# Output: cut.mp4, cutlist.json, cues.json (window + cues in CUT seconds, absolute).
import json, subprocess, re, sys

P = json.load(open(sys.argv[1], encoding="utf-8"))
KEEP, CUES = P["keep"], P.get("cues", {})

# compress pauses > 0.8 s inside kept ranges, keep 0.25 s each side
sil = subprocess.run(["ffmpeg", "-hide_banner", "-i", P["audio"], "-af", "silencedetect=noise=-38dB:d=0.8",
                      "-f", "null", "-"], capture_output=True, text=True).stderr
st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", sil)]
en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", sil)]
gaps = [(a + 0.25, b - 0.25) for a, b in zip(st, en)]

segs = []
for key, rs in KEEP.items():
    for a, b in rs:
        cur = a
        for ga, gb in gaps:
            if cur < ga and gb < b:
                segs.append((cur, ga, key)); cur = gb
        segs.append((cur, b, key))

t, mapped = 0.0, []
for a, b, k in segs:
    mapped.append((a, b, k, t)); t += b - a
total = t


def to_cut(x):
    for a, b, k, o in mapped:
        if a - 0.01 <= x <= b + 0.01:
            return o + (x - a)
    return [o for a, b, k, o in mapped if a > x][0]


order = list(KEEP)
starts = {k: min(o for a, b, kk, o in mapped if kk == k) for k in order}
cues = {}
for i, k in enumerate(order):
    s = starts[k]
    e = starts[order[i + 1]] if i + 1 < len(order) else total
    cues[k] = {"start": round(s, 3), "end": round(e, 3),
               "cues": {n: round(to_cut(v), 3) for n, v in CUES.get(k, {}).items()}}
json.dump(cues, open("cues.json", "w"), indent=1)
json.dump([{"src_in": round(a, 3), "src_out": round(b, 3), "q": k, "cut_at": round(o, 3)} for a, b, k, o in mapped],
          open("cutlist.json", "w"), indent=1)
print("segments", len(mapped), "total", round(total, 2))
for k in order:
    print(k, cues[k])

if "--render" in sys.argv:
    fc, n = [], len(mapped)
    for i, (a, b, k, o) in enumerate(mapped):
        d = b - a
        fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}];"
                  f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.02,afade=t=out:st={d - 0.03:.3f}:d=0.03[a{i}];")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    open("cut_fc.txt", "w").write("".join(fc))
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", P["src"],
                    "-filter_complex_script", "cut_fc.txt", "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", "-r", "30",
                    "-c:a", "aac", "-b:a", "192k", "cut.mp4"], check=True)

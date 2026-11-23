# Usage: python transcribe.py audio16k.wav out_prefix [model=medium] [chunk_sec=60]
# Chunked faster-whisper on CPU (int8). Low RAM: one model, 60 s chunks, retries on OOM.
import sys, json, time, subprocess, gc, wave
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
SIZE = sys.argv[3] if len(sys.argv) > 3 else "medium"
L = int(sys.argv[4]) if len(sys.argv) > 4 else 60
with wave.open(src) as w:
    dur = w.getnframes() / w.getframerate()
t0 = time.time()


def load():
    for k in range(10):
        try:
            return WhisperModel(SIZE, device="cpu", compute_type="int8", cpu_threads=4)
        except RuntimeError as e:
            print("load fail", k, e, flush=True); gc.collect(); time.sleep(20)
    raise SystemExit("cannot load")


m = load()
res = []
a = 0
while a < dur:
    b = min(a + L + 2, dur)
    wav = f"{out}_chunk.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", str(a), "-t", str(b - a), "-i", src, wav], check=True)
    for attempt in range(6):
        try:
            segs, _ = m.transcribe(wav, language="vi", word_timestamps=True, vad_filter=True, beam_size=5)
            part = [{"s": round(s.start + a, 2), "e": round(s.end + a, 2), "t": s.text.strip(),
                     "w": [[round(w.start + a, 2), round(w.end + a, 2), w.word] for w in (s.words or [])]} for s in segs]
            break
        except RuntimeError as e:
            print("chunk", a, "attempt", attempt, e, flush=True); gc.collect(); time.sleep(15)
    else:
        raise SystemExit("chunk failed")
    last = res[-1]["e"] - 0.05 if res else 0
    res += [x for x in part if x["s"] >= last]
    print("chunk", a, "ok", round(time.time() - t0), flush=True)
    a += L
json.dump(res, open(out + ".json", "w", encoding="utf-8"), ensure_ascii=False)
with open(out + ".txt", "w", encoding="utf-8") as f:
    for s in res:
        f.write(f"[{int(s['s'] // 60):02d}:{s['s'] % 60:05.2f}] {s['t']}\n")
print("done", len(res), round(time.time() - t0), "s")

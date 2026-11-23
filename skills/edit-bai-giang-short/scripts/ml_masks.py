# Usage: python ml_masks.py [threads]  -> ml/00000.png every 3rd frame of cut_crop.mov (u2net human seg)
import cv2, os, time, sys
from ort_matte import session, predict
STEP = 3
s = session("u2h", threads=int(sys.argv[1]) if len(sys.argv) > 1 else 4)
cap = cv2.VideoCapture("cut_crop.mov")
i, t0, n = 0, time.time(), 0
while True:
    ok, f = cap.read()
    if not ok: break
    out = f"ml/{i:05d}.png"
    if i % STEP == 0 and not os.path.exists(out):
        cv2.imwrite(out, (predict(s, "u2h", f) * 255).astype("uint8")); n += 1
        if n % 100 == 0: print(i, round(time.time() - t0), flush=True)
    i += 1
print("done", i, n, round(time.time() - t0), flush=True)

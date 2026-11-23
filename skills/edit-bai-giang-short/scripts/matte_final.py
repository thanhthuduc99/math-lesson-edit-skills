import cv2, numpy as np, os, sys, subprocess  # usage: python matte_final.py teacher_rgba.mov | test 120 600

STEP = 3
CW, CH = 440, 340  # crop size from make_crop.py
import json
CUTS = {round(x["out"][0] * 30) for x in json.load(open("cuts.json"))["segments"]}
K_DIL = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (71, 71))


def ml_at(i, n):
    k0 = (i // STEP) * STEP
    k1 = min(k0 + STEP, ((n - 1) // STEP) * STEP)
    m0 = cv2.imread(f"ml/{k0:05d}.png", 0).astype(np.float32) / 255
    if k1 == k0:
        return m0
    m1 = cv2.imread(f"ml/{k1:05d}.png", 0).astype(np.float32) / 255
    w = (i - k0) / (k1 - k0)
    for c in CUTS:
        if k0 < c <= k1:
            w = 0.0 if i < c else 1.0
    return m0 * (1 - w) + m1 * w


def raw_alpha(frame, m):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    dark = ((hsv[..., 2] < 115) & (hsv[..., 1] < 100)).astype(np.uint8)
    dark[:, CW - 15:] = 0  # crop edge: board strokes, not hair
    near = cv2.dilate((m > 0.5).astype(np.uint8), K_DIL)
    extra = cv2.medianBlur(dark * near * 255, 5).astype(np.float32) / 255
    a = np.maximum(m, extra)
    b = (a > 0.5).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(b, 8)
    if n > 1:
        big = 1 + np.argmax(st[1:, cv2.CC_STAT_AREA])
        keep = (lab == big).astype(np.uint8)
        a = a * cv2.dilate(keep, np.ones((9, 9), np.uint8))
        inv = (1 - keep).astype(np.uint8)
        nn, lab2, st2, _ = cv2.connectedComponentsWithStats(inv, 4)
        h, w = keep.shape
        for j in range(1, nn):
            x, y, ww, hh, area = st2[j]
            if x > 0 and y > 0 and x + ww < w and y + hh < h and area < 4000:
                a[lab2 == j] = 1.0
    return a


def finish(a):
    a = cv2.GaussianBlur(a, (0, 0), 1.2)
    return np.clip((a - 0.12) / 0.76, 0, 1)


def run(out_path, only=None):
    cap = cv2.VideoCapture("cut_crop.mov")
    frames = []
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    proc = None
    if only is None:
        proc = subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra",
                                 "-s", f"{CW}x{CH}", "-r", "30", "-i", "-", "-c:v", "png", out_path], stdin=subprocess.PIPE)
    prev = cur = None
    buf = []
    i = 0
    while True:
        ok, f = cap.read()
        if not ok:
            break
        if only is not None and not any(abs(i - o) <= 1 for o in only):
            i += 1
            continue
        a = raw_alpha(f, ml_at(i, n))
        buf.append((i, f, a))
        if len(buf) == 3:
            (_, _, a0), (ic, fc, a1), (_, _, a2) = buf
            if ic in CUTS:
                a0 = a1
            if ic + 1 in CUTS:
                a2 = a1
            emit(proc, ic, fc, finish(0.25 * a0 + 0.5 * a1 + 0.25 * a2), only)
            buf.pop(0)
        if i == 1 and only is None:
            emit(proc, 0, buf[0][1], finish(buf[0][2]), only)
        i += 1
    if only is None:
        emit(proc, buf[-1][0], buf[-1][1], finish(buf[-1][2]), only)
        proc.stdin.close()
        proc.wait()


def emit(proc, i, f, a, only):
    rgba = np.dstack([f, (a * 255).astype(np.uint8)])
    if only is not None:
        if i in only:
            cv2.imwrite(f"screens/matte_{i:05d}.png", rgba)
        return
    proc.stdin.write(rgba.tobytes())


if __name__ == "__main__":
    if sys.argv[1] == "test":
        run(None, [int(x) for x in sys.argv[2:]])
    else:
        run(sys.argv[1])

from pathlib import Path
import onnxruntime as ort, numpy as np, cv2, sys, time
MODELS = {"u2h": str(Path.home() / ".rembg/models/u2net_human_seg/u2net_human_seg.onnx"),
          "isnet": str(Path.home() / ".rembg/models/isnet-general-use/isnet-general-use.onnx")}

def session(name, threads=1):
    so = ort.SessionOptions()
    so.enable_cpu_mem_arena = False
    so.enable_mem_pattern = False
    so.intra_op_num_threads = threads
    so.inter_op_num_threads = 1
    return ort.InferenceSession(MODELS[name], so, providers=["CPUExecutionProvider"])

def predict(sess, name, bgr):
    size = 320 if name == "u2h" else 1024
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    x = cv2.resize(rgb, (size, size), interpolation=cv2.INTER_AREA).astype(np.float32)
    if name == "u2h":
        x = x / max(x.max(), 1e-6)
        x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    else:
        x = x / 255.0 - 0.5
    x = x.transpose(2, 0, 1)[None].astype(np.float32)
    out = sess.run(None, {sess.get_inputs()[0].name: x})[0][0, 0]
    out = (out - out.min()) / max(out.max() - out.min(), 1e-6)
    return cv2.resize(out, (bgr.shape[1], bgr.shape[0]), interpolation=cv2.INTER_LINEAR)


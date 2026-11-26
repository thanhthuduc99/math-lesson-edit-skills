# Usage: python chapters.py tx.json [chapters_draft.txt]
# Dò chỗ thầy nói "câu ..." trong transcript (tx.json của transcribe.py: [{"s","e","t"}...]) rồi ghi bản nháp
# timestamp: mỗi câu lấy lần nhắc đầu tiên, mốc cách nhau >= 10 s. Chỉ nhận câu kế tiếp (n = câu trước + 1); nói lại "câu 1" sau câu >= 4 = sang phần mới.
import json, re, sys

NUM = {"một": 1, "hai": 2, "ba": 3, "bốn": 4, "tư": 4, "năm": 5, "sáu": 6, "bảy": 7, "tám": 8, "chín": 9,
       "mười": 10, "mười một": 11, "mười hai": 12}
W = "|".join(sorted(NUM, key=len, reverse=True))
CAU = re.compile(rf"\bcâu (?:số )?(\d+|{W})\b", re.I)
PHAN = re.compile(r"\bphần (iii|ii|i|1|2|3|một|hai|ba)\b", re.I)


def ts(sec):
    sec = int(sec)
    h, m, s = sec // 3600, sec % 3600 // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


segs = json.load(open(sys.argv[1], encoding="utf-8"))
out = sys.argv[2] if len(sys.argv) > 2 else "chapters_draft.txt"
part, prev, seen, lines, last = 1, 0, set(), ["00:00 Giới thiệu đề"], 0
for g in segs:
    for m in CAU.finditer(g["t"].lower()):
        n = int(m[1]) if m[1].isdigit() else NUM[m[1]]
        if n == 1 and prev >= 4:
            part, prev = part + 1, 0
        if (part, n) in seen or n != prev + 1 and prev or g["s"] - last < 10:
            continue
        seen.add((part, n))
        prev, last = n, g["s"]
        roman = "I" * part if part < 4 else str(part)
        lines.append(f"{ts(g['s'])} Phần {roman}, câu {n}: <nội dung>    # \"{g['t'][:60]}\"")

open(out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines))

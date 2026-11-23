---
name: edit-bai-giang-dai
description: Edit video bài giảng toán dài (ngang 1920x1080, quay màn hình bảng + webcam giáo viên) bằng code. Giữ nguyên màn hình thầy live, chỉ cắt vấp và đè thêm card bài giải trắng (đồ thị, hình, các bước, ô đáp án, chip "Chọn X") vào vùng bảng trống, hiện theo đúng lời giảng. Không intro, không nhạc. Dùng khi user nói "edit video bài giảng dài", "thêm visual bài giải", "giữ màn hình thầy, thêm card lời giải", "edit video chữa đề dài".
---

# Edit bài giảng dài: màn hình live + card bài giải

Kết quả: video ngang 1920x1080, mở thẳng vào bài (không intro, không nhạc nền). Màn hình bảng và webcam của thầy giữ nguyên. Mỗi câu có 1 card trắng bo góc hiện lên vùng bảng trống, dựng lời giải theo đúng lúc thầy nói, rồi mờ đi trước khi sang câu sau.

Ví dụ: 4 câu trắc nghiệm, video 181.5 s, 4 card. Render 4 card mất 91 s, ghép 100 s trên máy 16 GB RAM.

## Cần có

- `ffmpeg`, Python 3.11+, `faster-whisper`, `numpy`, `Pillow`.
- Manim CE 0.22 (không cần LaTeX: chữ toán dùng font `Cambria Math` qua `Text`).
- Font Windows: Segoe UI, Cambria Math.

## Quy trình

Thư mục làm việc: copy `template/common.py`, `template/cards.py` và `scripts/` vào 1 folder `work/`.

### 1. Transcript

```bash
ffmpeg -i src.mp4 -ac 1 -ar 16000 audio16k.wav
python scripts/transcribe.py audio16k.wav tx medium
```

Chạy CPU int8, cắt chunk 60 s để không tràn RAM. Đọc `tx.txt`, đối chiếu với đáp án (PDF đề nếu có).

### 2. Cắt

Đọc transcript, ghi `plan.json`: mỗi câu là 1 key (`c1`, `c2`...), giữ các đoạn thầy giảng, bỏ câu vấp, câu bỏ dở, đoạn chờ. Ghi luôn mốc giây của từ khoá để card bám theo (vd lúc thầy nói "y(0) bằng âm 1").

```bash
python scripts/build_cut.py plan.json --render
```

Ra `cut.mp4` (khoảng lặng > 0.8 s rút còn 0.25 s mỗi bên) và `cues.json` (cửa sổ từng câu + mốc cue, tính theo giây của `cut.mp4`).

### 3. Tìm chỗ đặt card

```bash
python scripts/inkmap.py cut.mp4 cues.json screens/ink
```

Ảnh `ink_<câu>.jpg` là min từng pixel qua mọi khung hình của câu đó: mọi nét thầy từng viết đều hiện ra. Vùng còn sạch là chỗ đặt card. Script cũng in các mốc cuộn trang.

Luật đặt card:
- Không che chữ thầy đang viết hoặc đang chỉ vào. Che phần đề của câu khác thì được.
- Không che webcam (góc dưới phải) và đáp án A/B/C/D của câu đang chữa.
- Nếu trang cuộn giữa câu, card vào sau mốc cuộn.
- Toạ độ card ghi theo pixel 1920x1080: `card(x0, y0, x1, y1, n, title)`. Đổi pixel sang Manim: 135 px = 1 đơn vị.

### 4. Viết card

Mỗi câu là 1 class trong `cards.py`, kế thừa `CardScene`:
- `T0`: lúc card hiện (giây cut), `END`: lúc card mờ đi (trước khi sang câu sau ~0.2 s).
- `self.at(t)`: chờ tới giây `t` (giây cut, tuyệt đối) rồi mới chạy animation tiếp. Lấy `t` từ `cues.json`.
- Mẫu nội dung: tiêu đề ngắn trên header, hình bên trái (đồ thị `Axes`, tam giác, tiệm cận), các bước bên phải, kết quả màu xanh có `okbox`, chip `Chọn X`.
- Nền card trắng đặc (`fill_opacity=1`), không để bảng lộ qua.
- `cards.py` có sẵn 4 card mẫu: min trên đoạn, phương trình mũ, tổng vectơ, tiệm cận.

### 5. Duyệt ảnh tĩnh trước khi render

```bash
STILL=1 manim -s -t -q h cards.py Card1 Card2 Card3 Card4
python scripts/still_check.py cut.mp4 screens/still Card1=36 Card2=60.5 Card3=106.5 Card4=180
```

Mở `screens/still/still_sheet.jpg` xem: card có che chữ thầy, tràn khung, chữ đè nhau không. Gửi user duyệt sheet này trước khi render.

### 6. Render + ghép

```bash
manim -t --format=mov -q h cards.py Card1 Card2 Card3 Card4
bash scripts/mux.sh cut.mp4 ../out/long.mp4 Card1=3.4 Card2=43.9 Card3=71.6 Card4=114.6
```

Render tuần tự, không chạy 2 render song song trên máy 16 GB. Mux giữ tiếng gốc, chuẩn hoá -14 LUFS.

### 7. Kiểm tra

- Trích 6 khung rải đều ghép thành sheet, mở xem.
- `ffmpeg -i out.mp4 -af ebur128 -f null -` ra khoảng -14 LUFS.
- 1.5 s đầu có tiếng (video vào thẳng bài).

## Lỗi hay gặp

- Đặt tên class trùng hằng màu (vd `class C2`) làm hỏng màu `C2`. Đặt tên `Card1..N`.
- `Axes(numbers_to_include=...)` cần LaTeX. Tự đặt nhãn trục bằng `Text`.
- Bảng lộ qua card khi `fill_opacity` < 1.

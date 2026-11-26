---
name: edit-bai-giang-short
description: Cắt 1 câu, vài câu hoặc tất cả các câu trong video bài giảng toán ngang (bảng + webcam) thành video dọc TikTok 1080x1920 khoảng 2 phút. Dựng lại đề và lời giải bằng Manim (nền chấm, header logo, chip, tiêu đề lớn, hộp phụ đề), tách nền giáo viên từ webcam bằng u2net rồi đặt góc dưới phải. Không API trả phí. Dùng khi user nói "làm short bài giảng", "cắt video toán thành TikTok", "video dọc chữa đề", "edit short bài giảng", "làm short tất cả các câu".
---

# Edit bài giảng short: video dọc 1080x1920

Kết quả: video dọc ~2 phút cho 1 câu. Mỗi phần (Intro, Đề bài, Bước 1, Giải, Tóm tắt) là 1 scene Manim, chữ và hình hiện theo lời thầy. Thầy được tách nền từ webcam, đặt góc dưới phải, tiếng gốc.

Ví dụ: câu "tìm hàm bậc ba từ bảng số", 118.4 s, 5 scene.

## Cần có

- `ffmpeg`, Python 3.11+, `faster-whisper`, `numpy`, `opencv-python`, `onnxruntime`.
- Model `u2net_human_seg.onnx` ở `~/.rembg/models/u2net_human_seg/` (tải 1 lần qua `rembg` hoặc từ release của rembg).
- Manim CE 0.22. Font: Segoe UI, Segoe UI Black, Bahnschrift, Cambria Math.

## 2 cách dùng

- **Chọn câu**: "Từ video dài vừa edit, làm short câu 3, Phần II câu 1 và Phần III câu 5." Chạy quy trình dưới cho từng câu được nêu.
- **Tất cả các câu**: "Làm short tất cả các câu trong video `video.mp4`, đáp án ở `de.pdf`." Lấy mốc từng câu từ transcript cả video (dùng lại transcript của bước edit video dài, hoặc `youtube-title-description/scripts/chapters.py`), mỗi câu là 1 đoạn từ mốc câu đó tới mốc câu sau. Câu dài quá 3 phút thì rút gọn ở bước cắt vấp. Duyệt sheet ảnh tĩnh của tất cả short trong 1 lần, rồi render lần lượt từng short.

Mỗi short 1 folder con `short-<phần>-<câu>/`, ví dụ `short-p2-c1/`.

## Quy trình

Thư mục làm việc: copy `template/` (common.py, scenes.py, assets/) và `scripts/` vào 1 folder.

### 1. Chọn câu, transcript

```bash
ffmpeg -ss <bắt đầu> -to <kết thúc> -i src.mp4 -c:v libx264 -crf 14 -c:a pcm_s16le -ar 48000 seg.mp4
ffmpeg -i seg.mp4 -ac 1 -ar 16000 seg16k.wav
python scripts/transcribe.py seg16k.wav tx large-v3
```

Chọn câu có hình dễ dựng (đồ thị, bảng số, chuyển động) và lời giải gọn trong 2 phút.

### 2. Cắt vấp

Đọc `tx.txt`, ghi `keep.json` là danh sách đoạn giữ `[[a, b], ...]` (giây trong seg.mp4). Bỏ câu nói hỏng, câu lặp, đoạn chờ.

```bash
python scripts/cutlist.py keep.json seg16k.wav tx.json
python scripts/make_crop.py seg.mp4 1480 740        # góc trên-trái ô webcam trong khung 1920x1080
```

Ra `cuts.json`, `words_out.json` (giờ từng từ theo video đã cắt) và `cut_crop.mov` (ô webcam 440x340 + tiếng).

### 3. Tách nền giáo viên

```bash
mkdir ml && python scripts/ml_masks.py 4
python scripts/matte_final.py test 120 600 1500     # xem screens/matte_*.png
python scripts/matte_final.py teacher_rgba.mov
```

u2net chạy mỗi 3 khung, nội suy giữa 2 mask nhưng không nội suy qua điểm cắt. Thêm vùng tối gần người (tóc, áo đen), giữ khối lớn nhất, lấp lỗ nhỏ, làm mịn 3 khung.

### 4. Dựng scene

`template/common.py`:
- `BRAND, BRAND_URL, TEACHER` ở đầu file: đổi theo khách. `assets/badge_photo.png`: crop mặt thầy từ 1 khung webcam.
- Khối có sẵn: `header()` (logo + url + vạch), `top_block` / `swap_top` (chip nhỏ, tiêu đề lớn, tag), `set_caption` (hộp phụ đề dưới, 1–2 dòng), `chip`, `pill`, `shadow_box` (hộp viền đen đổ bóng), `badge()` (thẻ "GIẢNG BỞI"), `frac`, `M` (chữ toán Cambria Math).
- Màu: mực `#151515`, hồng `#D6246E`, nền chấm trắng.

`template/scenes.py` là ví dụ đủ 5 scene. Mỗi scene kế thừa `CueScene`, `self.at(t)` chờ tới giây `t` của video đã cắt. Lấy `t` từ `words_out.json`.

Bố cục khung dọc: header y≈6.5, tiêu đề y≈5, nội dung giữa, phụ đề y≈-3.55, phần dưới (~1/4 khung) để trống cho thầy.

Duyệt trước: `manim -s -q h scenes.py S2DeBai` ra ảnh tĩnh từng scene, ghép sheet gửi user duyệt rồi mới render.

### 5. Render + ghép

```bash
manim -q h scenes.py S1Intro S2DeBai S3Buoc1 S4Giai S5Ket
bash scripts/composite.sh ../out/short.mp4 S1Intro S2DeBai S3Buoc1 S4Giai S5Ket
```

Tổng thời lượng các scene phải khớp `cuts.json` → `total` (scene cuối chờ tới `total`). Render tuần tự trên máy 16 GB.

### 6. Kiểm tra

- Sheet 5 khung (1 khung mỗi scene): chữ không bị thầy che, phụ đề không tràn.
- Viền tách nền không nhấp nháy ở điểm cắt.
- Loudness khoảng -14 LUFS.

# Skills edit video bài giảng toán

3 skill Claude Code cho video chữa đề toán (quay màn hình bảng + webcam giáo viên), làm hoàn toàn bằng code: ffmpeg, faster-whisper, Manim, u2net, Pillow. Không dùng API trả phí.

| Skill | Đầu vào | Đầu ra |
|---|---|---|
| [`edit-bai-giang-dai`](skills/edit-bai-giang-dai/SKILL.md) | Video ngang nhiều câu | Video ngang, giữ màn hình thầy live, thêm card bài giải trắng vào vùng bảng trống |
| [`edit-bai-giang-short`](skills/edit-bai-giang-short/SKILL.md) | 1 câu trong video ngang | Video dọc 1080x1920 kiểu TikTok, dựng lại đề + lời giải, thầy tách nền góc dưới |
| [`thumbnail-bai-giang`](skills/thumbnail-bai-giang/SKILL.md) | PDF đề / bài giảng + ảnh thầy | Thumbnail 1280x720 style kênh thầy Đức + description YouTube |

## edit-bai-giang-dai

![4 khung hình video dài: card bài giải câu 1 đến câu 4 đặt trên vùng bảng trống, webcam thầy giữ nguyên góc dưới phải](docs/media/long_showcase.jpg)

Card hiện từng bước theo lời thầy: hình, các dòng biến đổi, kết quả đóng khung xanh, chip "Chọn X". Vị trí card chọn bằng "ink map" (min từng pixel qua cả câu) để không che chữ thầy viết.

<p><img width="480" src="docs/media/long_card.gif" alt="Card câu 3 dựng vectơ SO và dòng SB + SD = 2SO theo lời giảng"></p>

## edit-bai-giang-short

![5 khung hình video dọc: intro, đề bài, bước 1 lập hệ, thay t = 5, tóm tắt; thầy tách nền ở góc dưới phải](docs/media/short_showcase.jpg)

<p><img width="240" src="docs/media/short_clip.gif" alt="Đoạn short: điểm dữ liệu hiện lên đồ thị v(t) và hệ phương trình viết dần"></p>

## thumbnail-bai-giang

![10 thumbnail dựng bằng code: thanh tiêu đề màu có badge, 2 hình cắt từ PDF đề tô hồng, ảnh thầy ở giữa](docs/media/thumb_showcase.jpg)

Hình cắt thẳng từ PDF (`figs.py` quét ra toạ độ), nét đen đổi sang hồng. Mỗi tấm là 1 file JSON: tiêu đề, badge, màu thanh, 2 hình, ảnh thầy. 3 ảnh thầy tách nền có sẵn trong `teacher/`, mỗi tấm xoay vòng 1 ảnh. Font Montserrat tải riêng, xem SKILL.md.

## Cài

Copy thư mục skill vào `~/.claude/skills/`:

```bash
git clone https://github.com/thanhthuduc99/math-lesson-edit-skills
cp -r math-lesson-edit-skills/skills/* ~/.claude/skills/
```

Cần: `ffmpeg`, Python 3.11+, `manim` 0.22, `faster-whisper`, `opencv-python`, `onnxruntime`, `Pillow`, `pymupdf`. Font Windows: Segoe UI, Cambria Math, Bahnschrift.

## Hướng dẫn sử dụng

Quy trình chuẩn cho 1 buổi chữa đề: edit video dài trước, chọn câu hay cắt ra short, cuối cùng làm thumbnail. Bước nào cũng có ảnh mẫu để duyệt trước khi render, nên không mất thời gian render lại.

### 0. Chuẩn bị

Tạo 1 folder cho buổi đó, bỏ vào:

- Video quay gốc (ngang 1920x1080, bảng + webcam thầy).
- PDF đề có đáp án chi tiết. Claude đối chiếu đáp án với lời thầy và cắt hình từ đây làm thumbnail.
- Ảnh thầy PNG nền trong suốt (cho thumbnail), 2–3 ảnh để xoay vòng.

Mở Claude Code tại folder đó.

### 1. Edit video dài

Nói:

> Edit video bài giảng dài này: `video.mp4`, đề và đáp án ở `de.pdf`.

Claude sẽ:

1. Tách tiếng, chép lời thầy, đối chiếu với đáp án trong PDF.
2. Cắt vấp: bỏ câu nói hỏng, đoạn chờ, rút khoảng lặng.
3. Dựng card bài giải cho từng câu, gửi ảnh mẫu card đặt lên khung hình thật để bạn duyệt.
4. Bạn duyệt xong mới render ra video cuối.

Muốn sửa thì nói thẳng, vd "card câu 3 che chữ thầy, dời sang phải" hoặc "bỏ đoạn 12:30 đến 13:05".

### 2. Cắt short từ video dài

Xem video dài, chọn những câu bạn thích (câu có hình, lời giải gọn dưới 2 phút là đẹp nhất). Nói:

> Từ video dài vừa edit, cắt câu 3, Phần II câu 1 và Phần III câu 5 ra làm short.

Claude sẽ:

1. Tìm đoạn thầy giảng từng câu trong lời đã chép ở bước 1, cắt riêng từng đoạn ra.
2. Cắt vấp lần nữa cho gọn, tách nền thầy từ webcam.
3. Dựng lại đề + lời giải dạng dọc 1080x1920 cho từng câu, gửi ảnh mẫu từng cảnh để duyệt.
4. Duyệt xong render lần lượt từng short (render 1 cái 1 lần cho máy 16 GB không bị treo).

Không cần biết mốc giây, chỉ cần nói tên câu. Câu nào chưa thích thì nói "short câu 3 bỏ phần tóm tắt" hoặc "làm thêm câu 6".

### 3. Làm thumbnail

Khi video đã ổn, nói:

> Làm thumbnail cho video dài, tiêu đề "ĐỀ GIỮA HK1 NGUYỄN KHUYẾN", badge "2026-2027". Làm luôn thumbnail cho từng short và viết description YouTube.

Claude sẽ quét PDF ra danh sách hình, chọn 2 hình hợp tiêu đề, ghép ảnh thầy ở giữa, gửi ảnh để duyệt. Thumbnail dựng bằng code nên sửa rất nhanh: "đổi thanh màu xanh", "đổi hình bên phải thành câu bóng đèn", "dùng ảnh thầy cầm mic".

Description viết theo mẫu kênh thầy: câu đáng xem, nội dung video theo mốc giờ, đáp án nhanh, link tải đề.

### Mẹo

- Mỗi buổi 1 folder riêng, đừng để chung video của nhiều buổi.
- PDF đề càng rõ hình thì thumbnail càng đẹp. Đề toàn chữ thì gửi kèm PDF bài giảng có hình.
- Muốn làm lại từ đầu 1 bước, nói rõ bước đó: "edit lại video dài, giữ phần cắt cũ, chỉ đổi card".

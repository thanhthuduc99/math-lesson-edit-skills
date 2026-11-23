# Skills edit video bài giảng toán

2 skill Claude Code để edit video chữa đề toán (quay màn hình bảng + webcam giáo viên) hoàn toàn bằng code: ffmpeg, faster-whisper, Manim, u2net. Không dùng API trả phí.

| Skill | Đầu vào | Đầu ra |
|---|---|---|
| [`edit-bai-giang-dai`](skills/edit-bai-giang-dai/SKILL.md) | Video ngang nhiều câu | Video ngang, giữ màn hình thầy live, thêm card bài giải trắng vào vùng bảng trống |
| [`edit-bai-giang-short`](skills/edit-bai-giang-short/SKILL.md) | 1 câu trong video ngang | Video dọc 1080x1920 kiểu TikTok, dựng lại đề + lời giải, thầy tách nền góc dưới |

## edit-bai-giang-dai

![4 khung hình video dài: card bài giải câu 1 đến câu 4 đặt trên vùng bảng trống, webcam thầy giữ nguyên góc dưới phải](docs/media/long_showcase.jpg)

Card hiện từng bước theo lời thầy: hình, các dòng biến đổi, kết quả đóng khung xanh, chip "Chọn X". Vị trí card chọn bằng "ink map" (min từng pixel qua cả câu) để không che chữ thầy viết.

<p><img width="480" src="docs/media/long_card.gif" alt="Card câu 3 dựng vectơ SO và dòng SB + SD = 2SO theo lời giảng"></p>

## edit-bai-giang-short

![5 khung hình video dọc: intro, đề bài, bước 1 lập hệ, thay t = 5, tóm tắt; thầy tách nền ở góc dưới phải](docs/media/short_showcase.jpg)

<p><img width="240" src="docs/media/short_clip.gif" alt="Đoạn short: điểm dữ liệu hiện lên đồ thị v(t) và hệ phương trình viết dần"></p>

## Cài

Copy thư mục skill vào `~/.claude/skills/`:

```bash
git clone https://github.com/thanhthuduc99/math-lesson-edit-skills
cp -r math-lesson-edit-skills/skills/* ~/.claude/skills/
```

Cần: `ffmpeg`, Python 3.11+, `manim` 0.22, `faster-whisper`, `opencv-python`, `onnxruntime`, `Pillow`. Font Windows: Segoe UI, Cambria Math, Bahnschrift.

Rồi nói với Claude Code: "edit video bài giảng dài này" hoặc "làm short bài giảng từ câu 1".

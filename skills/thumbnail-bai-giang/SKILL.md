---
name: thumbnail-bai-giang
description: Dựng thumbnail YouTube 1280x720 cho video chữa đề / bài giảng toán theo style kênh thầy Đỗ Văn Đức hoàn toàn bằng code (Pillow + PyMuPDF), không dùng Codex hay API tạo ảnh. Hình cắt thẳng từ PDF đề hoặc bài giảng, tô hồng, ảnh thầy tách nền ở giữa xoay vòng, thanh tiêu đề màu + badge. Dùng khi user nói "làm thumbnail bài giảng", "thumbnail chữa đề", "thumbnail thầy Đức".
---

# Thumbnail bài giảng: code, không gen ảnh

Kết quả: ảnh 1280x720 nền trắng, thanh tiêu đề màu (y 43–165) có badge trắng bên phải, 2 hình cắt từ PDF hai bên tô hồng `#CD2674`, ảnh thầy tách nền ở giữa.

![10 thumbnail demo](../../docs/media/thumb_showcase.jpg)

## Cần có

- Python 3.11+, `pymupdf`, `Pillow`.
- `fonts/Montserrat-ExtraBold.ttf`: tải Montserrat từ Google Fonts (OFL), chép file ExtraBold vào `fonts/`.
- Kiểu chữ hẹp dùng Bahnschrift có sẵn trên Windows (`C:/Windows/Fonts/bahnschrift.ttf`).
- Ảnh thầy có sẵn trong `teacher/`: `thay-1.png` (khoanh tay), `thay-2.png` (cầm mic), `thay-3.png` (toàn thân, nơ bướm), PNG nền trong suốt. Mỗi tấm thumbnail lấy 1 ảnh, xoay vòng 1 → 2 → 3. Thêm ảnh mới thì đặt tên `thay-4.png`, thêm 1 dòng vào `keep.json`. `teacher/keep.json` ghi phần trên được giữ của từng ảnh: ảnh nửa người `1.0`, ảnh toàn thân cắt tới đùi khoảng `0.88` cho cỡ người đều nhau.

## Quy trình

### 1. Quét hình trong PDF

```bash
python figs.py de.pdf figs.jpg
```

In ra mỗi hình 1 dòng `{"page": p, "bbox": [x0, y0, x1, y1]}` và ghép `figs.jpg` có đánh số để chọn. Chỉ bắt được hình dạng ảnh. Bảng kẻ bằng nét vector thì tìm toạ độ bằng `page.search_for("chữ trong bảng")` rồi lấy khung các đường kẻ quanh đó.

Chọn hình:
- Hình gần vuông (khối chóp, lăng trụ, đồ thị, lưới điểm) đẹp nhất. Mỗi ô hình là 420x475.
- Bảng 2 dòng rất dẹt, thu vào ô thì chữ bé. Cắt còn cột tiêu đề + 1–2 cột số.
- Hình trong phần lời giải có nền hồng nhạt: thêm `"clear_bg": true`.

### 2. Viết config

```json
{"pdf": "de.pdf", "title": "ĐỀ GIỮA HK1 NGUYỄN KHUYẾN", "badge": "2026-2027", "bar": "pink",
 "figures": [{"page": 0, "bbox": [205, 306, 334, 412]}, {"page": 3, "bbox": [408, 513, 505, 610]}],
 "teacher": "teacher/thay-1.png", "out": "out/nguyen-khuyen.jpg"}
```

| Khóa | Giá trị |
|---|---|
| `bar` | `pink` `red` `blue` `purple`, mã hex, hoặc 2 màu chuyển `["#F7931E", "pink"]` |
| `badge` | `"2026-2027"`, `"số 01"`, `"LẦN 6"`, `"Cơ bản"`; bỏ trống thì tiêu đề căn giữa cả thanh |
| `font` | `wide` (Montserrat, mặc định) hoặc `condensed` (chữ hẹp cao, kiểu loạt "ĐỀ ÔN GIỮA HK1") |
| `badge_bg` | nền badge, kiểu chữ hẹp dùng vàng `#FFF4CC` |
| `figures[].clear_bg` | xoá nền hồng nhạt của hình |
| `figures[].bold` | độ dày nét (mặc định 3, `1` = giữ nguyên) |
| `figures[].pink` | `false` để giữ màu gốc |

Tiêu đề tự co cỡ để vừa ngang và vừa chiều cao thanh (tính cả dấu chồng như "Ề"). Badge ngắn (≤ 6 ký tự) chữ to gần bằng tiêu đề, badge dài như năm học chữ nhỏ. Xem 3 mẫu trong `configs/`.

### 3. Render và duyệt

```bash
python thumb.py configs/vi-du-mau-tron.json
```

Làm nhiều tấm: xoay vòng ảnh thầy (thay-1, thay-2, thay-3...), đổi màu thanh và kiểu badge giữa các tấm. Ghép sheet gửi user duyệt trước. Tự soát: dấu tiếng Việt không bị cắt, hình không chạm ảnh thầy, chữ trong bảng đọc được ở cỡ 640x360.

## Title, description, timestamp

Xem skill `youtube-title-description`.

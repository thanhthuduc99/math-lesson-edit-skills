---
name: youtube-title-description
description: Viết 3 title, description SEO và timestamp YouTube cho video chữa đề / bài giảng toán theo giọng kênh thầy Đỗ Văn Đức (@thayduc). Timestamp lấy từ transcript video thật, mỗi câu 1 mốc. Dùng khi user nói "viết title", "viết description", "làm timestamp", "mô tả YouTube video chữa đề".
---

# Title, description, timestamp YouTube

Đầu vào: video đã edit (hoặc video live), PDF đề có đáp án. Đầu ra: `youtube.txt` gồm 3 title để chọn + description dán thẳng vào YouTube.

Mẫu đầy đủ: `examples/description-nguyen-khuyen.txt`. Mẫu chuẩn trên kênh: video "Chữa đề giữa kì 1 Toán 12 Sở Hưng Yên 2026-2027 (mã 0113)", 13k view.

## 1. Timestamp (quan trọng nhất)

Timestamp tính trên đúng file sẽ đăng. Có transcript từ bước edit video dài thì dùng lại, chưa có thì chạy:

```bash
ffmpeg -i video.mp4 -ac 1 -ar 16000 a16k.wav
python ../edit-bai-giang-dai/scripts/transcribe.py a16k.wav tx small 120
python scripts/chapters.py tx.json chapters_draft.txt
```

`chapters.py` lấy lần đầu thầy nói "câu 1", "câu 2"... làm mốc. Nói lại "câu 1" sau câu 4 trở đi thì tính là sang phần mới. Mỗi dòng nháp kèm câu thầy nói để đối chiếu.

Sửa bản nháp thành bản cuối:
- Thay `<nội dung>` bằng chủ đề câu, lấy từ PDF đề, 4–10 chữ: `12:34 Phần II, câu 1: Lăng trụ tam giác đều: góc, khoảng cách, thể tích`.
- Câu thầy không nói rõ số thì xem khung hình quanh mốc đó (`ffmpeg -ss <giây> -i video.mp4 -frames:v 1 f.jpg`) để thêm hoặc sửa.
- Câu ngắn liền nhau có thể gộp: `Phần I, câu 1 đến 4: ...`.

Luật YouTube để hiện chapter: dòng đầu `00:00`, ít nhất 3 mốc, mỗi mốc cách nhau ≥ 10 giây, tăng dần. Qua 1 giờ ghi `1:02:24`.

## 2. 3 title để user chọn

Dưới 100 ký tự, có từ khoá chính (loại đề, lớp, trường, năm học), mỗi cái 1 góc:

1. Chuẩn SEO, mẫu Hưng Yên: `Chữa đề giữa kì 1 Toán 12 THPT <Trường> <Tỉnh> <Năm học> (mã <mã>) | Thầy Đỗ Văn Đức`.
2. Móc câu khó, mẫu TSA: `Chữa Đề Giữa Kì 1 Toán 12 <Trường> | <Câu phân loại, vd "Câu Phân Loại 17 Bóng Đèn"> | Thầy Đức`. Viết hoa chữ đầu mỗi từ.
3. Nhấn đáp án: `Đề giữa HK1 Toán 12 <Trường> <Tỉnh> (mã <mã>) | Đáp Án + Lời Giải Chi Tiết | Thầy Đỗ Văn Đức`.

Title bổ sung cho chữ trên thumbnail, không lặp nguyên văn.

## 3. Description

Thứ tự các khối:

1. 2 đoạn mở: tên đề, trường, ngày thi, mã đề; số câu, thời gian, cấu trúc 3 phần; đối tượng (2K9...) và kỳ thi hướng tới. Từ khoá chính nằm trong 2 câu đầu.
2. `🔥 NHỮNG CÂU ĐÁNG XEM NHẤT`: 4–6 dòng, mỗi dòng nêu câu + mấu chốt cách giải, có số liệu cụ thể.
3. `⏱️ NỘI DUNG VIDEO`: timestamp ở bước 1.
4. `✅ ĐÁP ÁN NHANH (MÃ ĐỀ ...)`: Phần I 1 dòng, Phần II từng câu a/b/c/d Đúng/Sai, Phần III 1 dòng. Lấy từ PDF lời giải, không tự giải lại.
5. `📄 Tải đề và lời giải: <link>` (chưa có link thì để `[LINK DRIVE ĐỀ]` và báo user), `📚 Khóa học Online môn Toán của thầy Đỗ Văn Đức: https://tenschool.vn`.
6. Câu kêu gọi like, đăng ký, để lại câu còn vướng ở bình luận.
7. 5–7 hashtag, vd `#Toan12 #2K9 #DeThiGiuaKi1 #<Truong> #<Tinh> #ThayDoVanDuc`.
8. Dòng `TAGS`: 10–15 cụm từ khoá cách nhau dấu phẩy (dán vào ô Tags trong Studio, không nằm trong description).

Description tối đa 5000 byte. Viết câu ngắn, không em dash, không câu sáo rỗng.

## 4. Giao

Ghi `youtube.txt` theo khuôn `examples/description-nguyen-khuyen.txt`, gửi user 3 title + description. Đăng tự động thì dùng skill `auto-post-youtube` (tuỳ chọn).

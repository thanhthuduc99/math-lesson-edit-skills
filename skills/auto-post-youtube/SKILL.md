---
name: auto-post-youtube
description: (Tuỳ chọn) Đăng video lên YouTube bằng YouTube Data API kèm title, description, thumbnail đã làm ở các skill trước. Mặc định để private, user tự bấm công khai trong Studio. Cần setup OAuth 1 lần. Dùng khi user nói "đăng YouTube", "up video lên kênh", "auto post".
---

# Auto-post YouTube (tuỳ chọn)

Skill này không bắt buộc. Không setup thì vẫn dùng được các skill khác, chỉ cần tự up video trong YouTube Studio và dán title, description, thumbnail vào.

## Setup 1 lần

1. Vào Google Cloud Console, tạo project, bật **YouTube Data API v3**.
2. OAuth consent screen: loại External, thêm email chủ kênh vào Test users.
3. Credentials → Create OAuth client ID → loại **Desktop app** → tải file JSON về, đặt tên `client_secret.json`.
4. Cài thư viện: `pip install google-api-python-client google-auth-oauthlib`.
5. Chạy trong folder làm việc:

   ```bash
   python scripts/get_token.py client_secret.json
   ```

   Trình duyệt mở ra, đăng nhập đúng tài khoản sở hữu kênh, cho phép. Script ghi 3 dòng `YOUTUBE_OAUTH_*` vào `.env`.

Không commit `.env` và `client_secret.json` lên git. Không dán các giá trị này vào chat.

## Đăng video

Chỉ chạy khi user đã chốt title (skill `youtube-title-description`). Ghi description cuối vào `description.txt` (bỏ dòng TAGS), rồi:

```bash
python scripts/upload_youtube.py video_final.mp4 "<title đã chốt>" description.txt --thumb thumbnail.jpg
```

- Mặc định `--privacy private`. Chỉ dùng `unlisted` hoặc `public` khi user nói rõ.
- Title tối đa 100 ký tự, description tối đa 5000 byte, script tự kiểm.
- Video dài up mất vài phút, chạy nền. Xong script in link `youtu.be/<id>` và link Studio để báo user.
- Thumbnail tự đặt chỉ được khi kênh đã xác minh số điện thoại.

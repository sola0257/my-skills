# Anti-Pattern: WeChat Article Publishing Failures (微信公众号发布失败案例)

## Case 1: Image Publishing Failure (2026-02-04)

### Problem Description
When publishing articles to WeChat Draft Box via API:
1.  **Base64 Failure in Metadata**: The `coverImage` field in the API payload rejects large Base64 strings (likely length limit), causing `PUBLISH_FAILED`.
2.  **URL Failure in Body**: Using external image URLs (e.g., ImgBB) in the article body HTML sometimes results in images not displaying in the WeChat editor (likely due to anti-hotlinking or filtering).

### Root Cause
- **API Limitation**: `coverImage` field expects a URL or small data, not a full 2MB+ Base64 string.
- **WeChat Content Filter**: The content editor is strict about external image sources in `<img>` tags.

### Solution (The "Hybrid Strategy")
We adopted a hybrid approach that satisfies both the API metadata requirements and the body content display requirements:

1.  **Cover Image (Metadata)**: Upload to a hosting service (ImgBB) and pass the **URL** to the `coverImage` API field.
    *   *Why*: Fits within API limits. Used only for the thumbnail in the article list.
2.  **Body Images (Content)**: Embed all images (including a copy of the cover) as **Base64 Data URIs** directly in the HTML `src` attribute.
    *   *Why*: Bypasses external link filtering. Ensures high quality and reliable display within the article body.
3.  **Dual Cover**: Explicitly insert the cover image at the top of the Markdown/HTML body so it appears as the first image in the article, ensuring the reader sees the high-quality version immediately.

### Code Pattern (Python)
```python
# 1. Upload cover to host for API field
cover_url = upload_to_host(cover_path)

# 2. Embed all images as Base64 in HTML body
img_tag = f'<img src="data:image/png;base64,..." ... />'
html_content = html_content.replace(markdown_image_ref, img_tag)

# 3. Construct Payload
payload = {
    "title": "...",
    "content": html_content, # Contains Base64 images
    "coverImage": cover_url  # Contains URL
}
```

---

## Case 2: Inappropriate Image Content (2026-02-04)

### Problem Description
1.  **Pinyin in Image**: The AI generated the text "Li Chun" (Pinyin for Start of Spring) on the cover image, which looked unprofessional for a Chinese cultural account.
2.  **Outdated Style**: The interior design style in generated images looked dated, not matching the current aesthetic trends.

### Root Cause
- **Loose Prompts**: The prompt didn't explicitly forbid text or specify a modern era.

### Solution
1.  **Negative Prompting**: Add `NO TEXT, NO PINYIN, NO WORDS` to the image prompt.
2.  **Style Enforcing**: Prepend style keywords like `Modern minimalist, 2024 design trends, bright and airy` to all interior scene prompts.

### Rule Update
Update `wechat-image-prompt-guide.md` to include these mandatory constraints.

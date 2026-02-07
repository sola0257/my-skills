---
name: xiaohongshu-content-generator
description: "Generate Xiaohongshu content. v10.0: Simplified & Progressive Disclosure. Knowledge base externalized."
license: MIT
version: "10.0"
---

## ⚠️ Recovery Execution Rules

**When user says "Continue Step X", "Next", "Proceed":**
1. ✅ Read the step description fully.
2. ✅ Check for required questions/confirmations.
3. ✅ Verify input parameters.
4. ✅ Ask if anything is missing.

**DO NOT assume context. DO NOT skip questions.**

---

## 📱 Platform Limits & Core Features

**Read:** `knowledge/xiaohongshu-platform-limits.md`
**Read:** `knowledge/xiaohongshu-core-features.md`

- **Visual Title**: Big text on cover.
- **Note Title**: SEO friendly, < 20 chars.
- **Body**: < 1000 chars, 5-step trust framework.
- **Images**: 12-15 images, 3:4 vertical.

---

## 🔍 Scenario Recognition [Mandatory]

### Scenario A: New Content ("Create", "Generate")
**Execute**: Workflow A (Step 0-12)

### Scenario B: Edit Content ("Modify", "Update")
**Execute**: Workflow B (Step E0-E6)
**Reference**: `_global_config/docs/workflows/content-editing-standards.md`

---

## 📝 Workflow A: New Content

### Step 0: Follower Engagement [Mandatory]
**⚠️ Read:** `knowledge/follower-engagement-guide.md`
1. **Ask User**: Current follower count (Use `AskUserQuestion`).
2. **Read History**: `粉丝数记录_小红书.json`.
3. **Action**: Generate encouragement, check 5-day stagnation.

### Step 1: Socratic Questioning [Mandatory]
**Ask**: Purpose, Topic Direction, Depth, Product Inclusion preferences.
**Reference**: `_global_config/docs/standards/intelligent-topic-selection-guide.md`

### Step 2: History Check [Mandatory]
**Action**: Read last 30 days of content to avoid duplicates.

### Step 3: Topic Selection [Mandatory]
**Action**: Propose topic based on user input + history check.

### Step 4: Knowledge Search [Silent]
**Action**: WebSearch + Local Knowledge Base for authority and depth.

### Step 5: Copy Generation [Silent]
**Action**: Generate Visual Title (3 options), Note Title, Body (5-step framework), Tags.
**Reference**: `_global_config/docs/standards/xiaohongshu-execution-standards.md`

### Step 5.5: Visual Title Confirmation [Mandatory]
**Action**: Ask user to select one visual title for the cover.

### Step 6: Value Check [Mandatory]
**⚠️ Read:** `knowledge/value-check-standards.md`
**Action**: Answer 6 self-check questions. If fail -> STOP.

### Step 7: Compliance Check [Silent]
**Action**: Use `compliance-checker` skill.

### Step 8: Product Matching [Silent, Unconditional]
**⚠️ Read:** `knowledge/product-matching-strategy.md`
**Action**: Match products, update Excel.
**Strategy**: 
- **0-500**: No mention in text.
- **500-2000**: Soft mention.
- **2000+**: Direct link/price.

### Step 9: Image Generation [Silent]
**⚠️ Read:** `knowledge/image-prompt-guide.md`
**Action**: Generate 12-15 images (1 Cover + 11-14 Content).
**Tool**: `_shared_scripts/yunwu_image_api.py` (Gemini model).
**Cover**: Must match selected Visual Title text.

### Step 10: Save Files [Silent]
**Action**: Save .md, .txt (release version), images, data.json.
**Path**: `/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/小红书/`

### Step 11: Satisfaction Check & Loop [Mandatory]
**Action**: Ask satisfaction (1-5).
- **≤ 3**: Ask "Which part?" -> Jump back to Step 2/5/8/9 -> Loop.
- **≥ 4**: Record to `successful-cases`, Ask "Push now?".

---

## ✏️ Workflow B: Edit Content

### Step E0-E2: Identify & Ask
**Action**: Read existing content, ask what to change.

### Step E3: Execute Change [Silent]
**Action**: Modify content/images.

### Step E4: Quality Assurance [Mandatory]
**⚠️ Read:** `knowledge/value-check-standards.md`
**Action**: Full check (Title, Images, Compliance, Strategy).

### Step E5-E6: Save & Finalize
**Action**: Save files, ask to push.

---

## 📦 Output Structure

**Format**:
- `_发布版.txt`: Plain text for copy-paste.
- `.md`: Archive with metadata.
- Images: `cover_final.png`, `01.png`...

**Reference**: `knowledge/xiaohongshu-core-features.md`

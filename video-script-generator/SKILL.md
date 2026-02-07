---
name: video-script-generator
description: "Generate short video scripts for all platforms. v4.0: Simplified & Progressive Disclosure. Knowledge base externalized."
license: MIT
version: "4.0"
---

## ⚠️ Recovery Execution Rules

**When user says "Continue Step X", "Next", "Proceed":**
1. ✅ Read the step description fully.
2. ✅ Check for required questions/confirmations.
3. ✅ Verify input parameters.
4. ✅ Ask if anything is missing.

**DO NOT assume context. DO NOT skip questions.**

---

## 🎬 Types & Platforms

**Read:** `knowledge/video_platform_strategy.md`

### Types
- **Knowledge Share**: Hook + Points + Summary (1-3 min).
- **Life Insight**: Scene + Emotion + Golden Sentence (30s-1 min).

### Platforms & Cover Sizes
- **Xiaohongshu/Video**: 3:4 Vertical (1080x1440).
- **Douyin/Kuaishou**: 9:16 Vertical (1080x1920).

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
2. **Read History**: `粉丝数记录_{平台}.json`.
3. **Action**: Generate encouragement, check 5-day stagnation.

### Step 1: Socratic Questioning [Mandatory]
**Ask**: Type, Platform, Duration, Purpose, Topic, Depth, Product preference.
**Reference**: `_global_config/docs/standards/intelligent-topic-selection-guide.md`

### Step 2: History Check [Mandatory]
**Action**: Read last 30 days of content to avoid duplicates.

### Step 3: Topic Selection [Mandatory]
**Action**: Propose topic based on user input + history check.

### Step 4: Knowledge Search [Mandatory]
**Action**: WebSearch + Local Knowledge Base.
**Requirement**: Deep/Scientific content must be verified.

### Step 5: Parse Input [Silent]
**Action**: Determine final Type, Platforms, Duration.

### Step 6: Value Check [Mandatory]
**⚠️ Read:** `knowledge/value-check-standards.md`
**Action**: Answer 6 self-check questions. If fail -> STOP.

### Step 7: Product Matching [Silent, Unconditional]
**⚠️ Read:** `knowledge/product-matching-strategy.md`
**Action**: Match products, update Excel.
**Strategy**: 
- **0-500**: No mention.
- **500-2000**: Soft mention (1-2 times in script).
- **2000+**: Direct mention/link.

### Step 8: Generate Storyboard [Silent]
**Action**: Create 3-8 scenes (Visual + Audio + Duration).

### Step 9: Generate Verbatim Script [Silent]
**Action**: Write natural spoken script for each scene.

### Step 10: Generate Images [Silent]
**⚠️ Read:** `knowledge/video-image-prompt-guide.md`
**Action**: 
1. Generate Scene images (3:4 or 9:16 based on primary platform).
2. Generate **4 separate Covers** (2 sizes x 2 styles if needed).
**Tool**: `../_shared_scripts/yunwu_image_api.py`

### Step 11: Save Files [Silent]
**Action**: Save scripts (.md), images (folders), data.json.
**Path**: `/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/视频脚本/`

### Step 12: Satisfaction Check & Loop [Mandatory]
**Action**: Ask satisfaction (1-5).
- **≤ 3**: Ask "Which part?" -> Jump back -> Loop.
- **≥ 4**: Record to `successful-cases`, End task.

---

## ✏️ Workflow B: Edit Content

### Step E0-E2: Identify & Ask
**Action**: Read existing script, ask what to change.

### Step E3: Execute Change [Silent]
**Action**: Modify script/images.

### Step E4: Quality Assurance [Mandatory]
**⚠️ Read:** `knowledge/value-check-standards.md`
**Action**: Full check (Structure, Flow, Compliance, Strategy).

### Step E5-E6: Save & Finalize
**Action**: Save files, ask to publish (manual).

---

## 📦 Output Structure

**Files**:
- `_分镜脚本.md`
- `_逐字稿.md`
- `分镜配图/` (01.png...)
- `封面/` (Xiaohongshu.png, Douyin.png...)
- `data.json`

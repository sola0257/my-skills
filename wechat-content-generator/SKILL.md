---
name: wechat-content-generator
description: "Generate WeChat Official Account content. v5.0: Simplified & Progressive Disclosure. Knowledge base externalized."
license: MIT
version: "5.0"
---

## ⚠️ Recovery Execution Rules

**When user says "Continue Step X", "Next", "Proceed":**
1. ✅ Read the step description fully.
2. ✅ Check for required questions/confirmations.
3. ✅ Verify input parameters.
4. ✅ Ask if anything is missing.

**DO NOT assume context. DO NOT skip questions.**

---

## 📱 Platform & Formats

**Read:** `knowledge/wechat_strategy_handbook.md`

### Formats
- **Long Article**: 1 Cover (2.35:1) + 3 Body Images (16:9).
- **Image-Text**: 1 Cover (3:4) + 5 Body Images (3:4).
- **Default**: Long Article if not specified.

### Accounts
- **Subscription**: Knowledge, Emotional, Soft sell.
- **Service**: Product, Service, Direct sell.

---

## 🔍 Scenario Recognition [Mandatory]

### Scenario A: New Content ("Create", "Generate")
**Execute**: Workflow A (Step 0-13)

### Scenario B: Edit Content ("Modify", "Update")
**Execute**: Workflow B (Step E0-E6)
**Reference**: `_global_config/docs/workflows/content-editing-standards.md`

---

## 📝 Workflow A: New Content

### Step 0: Follower Engagement [Mandatory]
**⚠️ Read:** `knowledge/follower-engagement-guide.md`
1. **Ask User**: Current follower count (Use `AskUserQuestion`).
2. **Read History**: `粉丝数记录_公众号.json`.
3. **Action**: Generate encouragement, check 5-day stagnation.

### Step 1: Socratic Questioning [Mandatory]
**Ask**: Format, Platform, Purpose, Topic, Depth, Product preference.
**Reference**: `_global_config/docs/standards/intelligent-topic-selection-guide.md`

### Step 2: History Check [Mandatory]
**Action**: Read last 30 days of content to avoid duplicates.

### Step 3: Topic Selection [Mandatory]
**Action**: Propose topic based on user input + history check.

### Step 4: Knowledge Search [Mandatory]
**Action**: WebSearch (Mandatory for deep content) + Local Knowledge Base.
**If Search Fails**: Report to user and ask to continue or not.

### Step 5: Copy Generation [Silent]
**Action**: Generate Title, Abstract, Body (Structure depends on Format), CTA.
**Reference**: `knowledge/subscription-copywriting.md`

### Step 6: Value Check [Mandatory]
**⚠️ Read:** `knowledge/value-check-standards.md`
**Action**: Answer 6 self-check questions. If fail -> STOP.

### Step 7: Compliance Check [Silent]
**Action**: Use `compliance-checker` skill.

### Step 8: Product Matching [Silent, Unconditional]
**⚠️ Read:** `knowledge/product-matching-strategy.md`
**Action**: Match products, update Excel.
**Strategy**: 0-500 (No mention), 500-2000 (Soft), 2000+ (Direct).

### Step 9: Image Generation [Silent]
**⚠️ Read:** `knowledge/image-generation-dynamic-count.md`
**Action**: Generate images based on Format (Long vs Image-Text).
**Tool**: `scripts/generate_wechat_images.py`
**Reference**: `knowledge/wechat-image-prompt-guide.md`

### Step 10: Save Files [Silent]
**Action**: Save .md, images, data.json to specific folder.

### Step 11: Pre-Publish Check [Mandatory]
**⚠️ Read:** `knowledge/pre-publish-checklist.md`
**Action**: Check file integrity, image specs, push params.
**If Fail**: STOP and report.

### Step 12: Publish to Drafts [Silent]
**Action**: Call `scripts/wechat_publish.py`
**Strategy**: Hybrid (Cover via URL, Body via Base64).

### Step 13: Satisfaction Check & Loop [Mandatory]
**Action**: Ask satisfaction (1-5).
- **≤ 3**: Ask "Which part?" -> Jump back -> Loop.
- **≥ 4**: Record to `successful-cases`, End task.

---

## ✏️ Workflow B: Edit Content

### Step E0-E2: Identify & Ask
**Action**: Read existing content, ask what to change.

### Step E3: Execute Change [Silent]
**Action**: Modify content/images.

### Step E4: Quality Assurance [Mandatory]
**⚠️ Read:** `knowledge/value-check-standards.md`
**Action**: Full check (Title, Images, Compliance, Strategy).

### Step E5-E6: Save & Republish
**Action**: Save files, ask to push again.

---

## 📦 Output Structure

**Path**: `/Users/dj/Desktop/全域自媒体运营/内容发布/发布记录/2026/订阅号/`
**Files**: .md, cover.png, 01.png..., data.json

**Reference**: `knowledge/wechat_strategy_handbook.md`

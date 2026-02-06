# Xiaohongshu Visual Platform - Implementation Plan (精简版)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local MVP for Xiaohongshu content management with Vue 3 frontend and Python backend

**Architecture:** Frontend-first SPA with Vue 3 + Vite, Python backend calling xiaohongshu-content-generator skill, local JSON storage

**Tech Stack:** Vue 3, Vite, Tailwind CSS, Vue Router, Python 3, Node.js

---

## Task 1: Project Initialization

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/tailwind.config.js`

**Steps:**
1. Create directory structure: `frontend/src/{views,components,api,router}`, `backend`, `data/{contents,images}`
2. Initialize Vite project: `npm create vite@latest frontend -- --template vue`
3. Install dependencies: `npm install && npm install -D tailwindcss postcss autoprefixer vue-router`
4. Initialize Tailwind: `npx tailwindcss init -p`
5. Configure Tailwind content paths in `tailwind.config.js`
6. Import Tailwind in `src/style.css`
7. Test: `npm run dev` - should see Vite welcome page
8. Commit: `git init && git add . && git commit -m "feat: initialize project structure"`

---

## Task 2: Router Setup

**Files:**
- Create: `frontend/src/router/index.js`
- Modify: `frontend/src/main.js`

**Steps:**
1. Create router with 3 routes: `/` (home), `/create` (create), `/list` (list)
2. Configure history mode
3. Register router in main.js
4. Test: Navigate to each route - should see route changes
5. Commit: `git add . && git commit -m "feat: add Vue Router with basic routes"`

---

## Task 3: Layout Component

**Files:**
- Create: `frontend/src/components/AppLayout.vue`
- Modify: `frontend/src/App.vue`

**Steps:**
1. Create AppLayout with header, sidebar, main content area
2. Add navigation links (首页, 创建内容, 内容列表)
3. Use Tailwind for styling (sidebar: w-64, bg-gray-800)
4. Wrap router-view in AppLayout
5. Test: Navigation should work, layout should be responsive
6. Commit: `git add . && git commit -m "feat: add app layout with navigation"`

---

## Task 4: Home Page

**Files:**
- Create: `frontend/src/views/HomeView.vue`

**Steps:**
1. Create welcome section with project title
2. Add 3 feature cards (快速生成, 可视化管理, 本地存储)
3. Add "开始创建" button linking to /create
4. Style with Tailwind (cards: grid grid-cols-3 gap-6)
5. Test: Should see welcome page with cards
6. Commit: `git add . && git commit -m "feat: add home page with feature cards"`

---

## Task 5: Content List Page (Static)

**Files:**
- Create: `frontend/src/views/ContentListView.vue`
- Create: `frontend/src/components/ContentCard.vue`

**Steps:**
1. Create ContentCard component (shows title, date, status, thumbnail)
2. Create ContentListView with grid layout
3. Add mock data (3 sample contents)
4. Add filter buttons (全部, 草稿, 已发布)
5. Test: Should see 3 content cards in grid
6. Commit: `git add . && git commit -m "feat: add content list page with mock data"`

---

## Task 6: API Module (Mock)

**Files:**
- Create: `frontend/src/api/content.js`

**Steps:**
1. Create `generateContent(topic)` - returns mock content after 2s delay
2. Create `generateImages(prompts, onProgress)` - simulates image generation with progress
3. Create `saveContent(content)` - logs to console
4. Create `listContents()` - returns mock array
5. Test: Call functions in console - should work with delays
6. Commit: `git add . && git commit -m "feat: add mock API module"`

---

## Task 7: Create Page Components

**Files:**
- Create: `frontend/src/components/TopicInput.vue`
- Create: `frontend/src/components/ResultPreview.vue`
- Create: `frontend/src/components/ProgressModal.vue`

**Steps:**
1. TopicInput: textarea + generate button
2. ResultPreview: displays title, content, 12 images in grid, action buttons
3. ProgressModal: shows progress bar, current step, message
4. Test each component in isolation
5. Commit: `git add . && git commit -m "feat: add create page components"`

---

## Task 8: Create Page Integration

**Files:**
- Create: `frontend/src/views/CreateView.vue`

**Steps:**
1. Import all 3 components (TopicInput, ResultPreview, ProgressModal)
2. Implement handleGenerate: calls API, shows progress modal, updates result
3. Implement handleSave: saves content, navigates to /list
4. Implement handleEdit, handleDiscard, handleRegenerateSingle
5. Test: Enter topic → see progress → see result → save → navigate to list
6. Commit: `git add . && git commit -m "feat: add content create page with mock API"`

---

## Task 9: Backend API Setup

**Files:**
- Create: `backend/app.py`
- Create: `backend/requirements.txt`
- Create: `backend/.env.example`

**Steps:**
1. Create requirements.txt (flask, flask-cors, python-dotenv)
2. Create Flask app with CORS enabled
3. Add routes: `/api/health`, `/api/generate`, `/api/contents` (GET/POST), `/api/contents/<id>`
4. Use mock data for now (no skill integration yet)
5. Test: `python app.py` → curl endpoints → should return JSON
6. Commit: `git add . && git commit -m "feat: add Flask backend with basic API endpoints"`

---

## Task 10: Data Storage Module

**Files:**
- Create: `backend/storage.py`
- Modify: `backend/app.py`

**Steps:**
1. Create functions: `save_content`, `get_content`, `list_contents`, `delete_content`, `save_image`
2. Use JSON files in `data/contents/` directory
3. Update app.py to use storage module
4. Test: POST content → check JSON file created → GET content → should match
5. Commit: `git add . && git commit -m "feat: add data storage module for JSON persistence"`

---

## Task 11: Connect Frontend to Backend

**Files:**
- Modify: `frontend/src/api/content.js`
- Modify: `frontend/vite.config.js`

**Steps:**
1. Add proxy config in vite.config.js: `/api` → `http://localhost:5000`
2. Replace mock API with real fetch calls
3. Update error handling
4. Test: Start backend → start frontend → generate content → should call real API
5. Commit: `git add . && git commit -m "feat: connect frontend to backend API"`

---

## Task 12: Skill Integration

**Files:**
- Create: `backend/skill_caller.py`
- Modify: `backend/app.py`

**Steps:**
1. Create `call_xiaohongshu_skill(topic)` function
2. Use subprocess to call Claude Code with skill
3. Parse skill output (JSON format)
4. Update `/api/generate` endpoint to use skill_caller
5. Test: Generate content → should call real skill → return actual content
6. Commit: `git add . && git commit -m "feat: integrate xiaohongshu-content-generator skill"`

---

## Task 13: Image Handling

**Files:**
- Modify: `backend/storage.py`
- Modify: `backend/app.py`
- Modify: `frontend/src/components/ResultPreview.vue`

**Steps:**
1. Add image upload endpoint: `/api/images`
2. Save images to `data/images/` with unique filenames
3. Return image URLs in content response
4. Update frontend to display real images
5. Test: Generate content → images should be saved and displayed
6. Commit: `git add . && git commit -m "feat: add image upload and storage"`

---

## Task 14: Content List Integration

**Files:**
- Modify: `frontend/src/views/ContentListView.vue`

**Steps:**
1. Replace mock data with API call to `/api/contents`
2. Add loading state
3. Add error handling
4. Implement filter functionality (filter by status)
5. Test: Should load real contents from backend
6. Commit: `git add . && git commit -m "feat: integrate content list with backend"`

---

## Task 15: Content Detail View

**Files:**
- Create: `frontend/src/views/ContentDetailView.vue`
- Modify: `frontend/src/router/index.js`

**Steps:**
1. Add route: `/content/:id`
2. Create detail view showing full content
3. Add edit/delete buttons
4. Fetch content by ID from API
5. Test: Click content card → navigate to detail → see full content
6. Commit: `git add . && git commit -m "feat: add content detail view"`

---

## Task 16: Edit Functionality

**Files:**
- Modify: `frontend/src/views/CreateView.vue`
- Modify: `backend/app.py`

**Steps:**
1. Add edit mode to CreateView (load existing content)
2. Add PUT endpoint: `/api/contents/<id>`
3. Update save logic to handle both create and update
4. Test: Edit content → save → should update existing content
5. Commit: `git add . && git commit -m "feat: add content edit functionality"`

---

## Task 17: Delete Functionality

**Files:**
- Modify: `frontend/src/views/ContentDetailView.vue`
- Modify: `backend/app.py`

**Steps:**
1. Add DELETE endpoint: `/api/contents/<id>`
2. Add delete confirmation dialog
3. Implement delete handler in frontend
4. Test: Delete content → should remove from list
5. Commit: `git add . && git commit -m "feat: add content delete functionality"`

---

## Task 18: Error Handling & Loading States

**Files:**
- Modify: `frontend/src/api/content.js`
- Modify: All view components

**Steps:**
1. Add try-catch blocks to all API calls
2. Add loading spinners to all async operations
3. Add error toast notifications
4. Add empty states (no contents yet)
5. Test: Simulate errors → should show error messages
6. Commit: `git add . && git commit -m "feat: improve error handling and loading states"`

---

## Task 19: Polish UI/UX

**Files:**
- Modify: All component files

**Steps:**
1. Add transitions and animations
2. Improve responsive design (mobile-friendly)
3. Add hover effects and focus states
4. Improve color scheme and typography
5. Test: Should look polished and professional
6. Commit: `git add . && git commit -m "style: polish UI/UX with animations and responsive design"`

---

## Task 20: Documentation & README

**Files:**
- Create: `README.md`
- Create: `docs/SETUP.md`
- Create: `docs/API.md`

**Steps:**
1. Write README with project overview, features, tech stack
2. Write setup instructions (installation, running, configuration)
3. Document API endpoints
4. Add screenshots
5. Test: Follow setup instructions on fresh machine
6. Commit: `git add . && git commit -m "docs: add comprehensive documentation"`

---

## Execution Handoff

**Plan complete and saved to `docs/plans/2026-02-06-implementation-plan-v2.md`. Two execution options:**

**1. Subagent-Driven (this session)** - I dispatch fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** - Open new session with executing-plans, batch execution with checkpoints

**Which approach?**

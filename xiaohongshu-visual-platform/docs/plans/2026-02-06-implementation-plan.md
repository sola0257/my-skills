# Xiaohongshu Visual Platform - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a local MVP for Xiaohongshu content management with Vue 3 frontend and Python backend

**Architecture:** Frontend-first SPA with Vue 3 + Vite, Python backend calling xiaohongshu-content-generator skill, local JSON storage

**Tech Stack:** Vue 3, Vite, Tailwind CSS, Vue Router, Python 3, Node.js

---

## Task 1: Project Initialization

**Files:**
- Create: `frontend/package.json`
- Create: `frontend/vite.config.js`
- Create: `frontend/index.html`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/postcss.config.js`

**Step 1: Create project directory structure**

Run: `cd /Users/dj/Desktop/小静的skills/xiaohongshu-visual-platform && mkdir -p frontend/src/{views,components,api,router} backend data/{contents,images}`

**Step 2: Initialize frontend with Vite**

Run: `cd frontend && npm create vite@latest . -- --template vue`
Expected: Vite project scaffolding created

**Step 3: Install dependencies**

Run: `npm install && npm install -D tailwindcss postcss autoprefixer vue-router`
Expected: Dependencies installed successfully

**Step 4: Initialize Tailwind CSS**

Run: `npx tailwindcss init -p`
Expected: tailwind.config.js and postcss.config.js created

**Step 5: Configure Tailwind**

Edit `frontend/tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{vue,js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Step 6: Add Tailwind directives to CSS**

Create `frontend/src/style.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**Step 7: Commit**

```bash
git add .
git commit -m "feat: initialize Vue 3 + Vite + Tailwind project"
```

---

## Task 2: Frontend Entry Point Setup

**Files:**
- Modify: `frontend/src/main.js`
- Modify: `frontend/src/App.vue`
- Create: `frontend/src/router/index.js`

**Step 1: Configure main.js**

Edit `frontend/src/main.js`:
```javascript
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'

createApp(App)
  .use(router)
  .mount('#app')
```

**Step 2: Create router configuration**

Create `frontend/src/router/index.js`:
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import ContentCreate from '../views/ContentCreate.vue'
import ContentList from '../views/ContentList.vue'
import ContentDetail from '../views/ContentDetail.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/create',
    name: 'ContentCreate',
    component: ContentCreate
  },
  {
    path: '/list',
    name: 'ContentList',
    component: ContentList
  },
  {
    path: '/detail/:id',
    name: 'ContentDetail',
    component: ContentDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
```

**Step 3: Update App.vue**

Edit `frontend/src/App.vue`:
```vue
<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <router-view />
  </div>
</template>

<script setup>
</script>
```

**Step 4: Commit**

```bash
git add .
git commit -m "feat: setup router and app structure"
```

---

## Task 3: Home Page (Navigation)

**Files:**
- Create: `frontend/src/views/Home.vue`

**Step 1: Create Home page component**

Create `frontend/src/views/Home.vue`:
```vue
<template>
  <div class="container mx-auto px-4 py-16">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-bold text-center mb-4 text-gray-800">
        小红书内容管理平台
      </h1>
      <p class="text-center text-gray-600 mb-12">
        快速生成高质量的小红书内容
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Create Content Card -->
        <router-link
          to="/create"
          class="block p-8 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow"
        >
          <div class="text-5xl mb-4">✨</div>
          <h2 class="text-2xl font-semibold mb-2">创建内容</h2>
          <p class="text-gray-600">
            输入选题，自动生成文案和配图
          </p>
        </router-link>

        <!-- View Content Card -->
        <router-link
          to="/list"
          class="block p-8 bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow"
        >
          <div class="text-5xl mb-4">📋</div>
          <h2 class="text-2xl font-semibold mb-2">内容列表</h2>
          <p class="text-gray-600">
            查看和管理已生成的内容
          </p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
</script>
```

**Step 2: Test the page**

Run: `npm run dev`
Expected: Dev server starts, navigate to http://localhost:5173 and see home page

**Step 3: Commit**

```bash
git add .
git commit -m "feat: add home page with navigation"
```

---

## Task 4: Topic Input Component

**Files:**
- Create: `frontend/src/components/TopicInput.vue`

**Step 1: Create TopicInput component**

Create `frontend/src/components/TopicInput.vue`:
```vue
<template>
  <div class="w-full">
    <label class="block text-sm font-medium text-gray-700 mb-2">
      选题
    </label>
    <div class="flex gap-3">
      <input
        v-model="localTopic"
        type="text"
        placeholder="例如：多肉植物养护技巧"
        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        @keyup.enter="handleSubmit"
      />
      <button
        @click="handleSubmit"
        :disabled="!localTopic.trim() || loading"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
      >
        {{ loading ? '生成中...' : '生成内容' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: String,
  loading: Boolean
})

const emit = defineEmits(['update:modelValue', 'submit'])

const localTopic = ref(props.modelValue || '')

watch(() => props.modelValue, (newVal) => {
  localTopic.value = newVal
})

watch(localTopic, (newVal) => {
  emit('update:modelValue', newVal)
})

const handleSubmit = () => {
  if (localTopic.value.trim() && !props.loading) {
    emit('submit', localTopic.value.trim())
  }
}
</script>
```

**Step 2: Commit**

```bash
git add .
git commit -m "feat: add topic input component"
```

---

## Task 5: Progress Modal Component

**Files:**
- Create: `frontend/src/components/ProgressModal.vue`

**Step 1: Create ProgressModal component**

Create `frontend/src/components/ProgressModal.vue`:
```vue
<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
  >
    <div class="bg-white rounded-lg p-8 max-w-md w-full mx-4">
      <h3 class="text-xl font-semibold mb-4 text-center">
        {{ title }}
      </h3>

      <!-- Progress Bar -->
      <div class="mb-4">
        <div class="w-full bg-gray-200 rounded-full h-3">
          <div
            class="bg-blue-600 h-3 rounded-full transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <p class="text-sm text-gray-600 text-center mt-2">
          {{ progress }}%
        </p>
      </div>

      <!-- Status Message -->
      <p class="text-center text-gray-700 mb-4">
        {{ message }}
      </p>

      <!-- Current Step -->
      <div v-if="currentStep" class="text-sm text-gray-500 text-center">
        {{ currentStep }}
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: {
    type: String,
    default: '正在生成内容'
  },
  progress: {
    type: Number,
    default: 0
  },
  message: {
    type: String,
    default: '请稍候...'
  },
  currentStep: String
})
</script>
```

**Step 2: Commit**

```bash
git add .
git commit -m "feat: add progress modal component"
```

---

## Task 6: Image Gallery Component

**Files:**
- Create: `frontend/src/components/ImageGallery.vue`

**Step 1: Create ImageGallery component**

Create `frontend/src/components/ImageGallery.vue`:
```vue
<template>
  <div class="w-full">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-semibold">
        配图 ({{ successCount }}/{{ images.length }} 张成功)
      </h3>
      <button
        v-if="failedImages.length > 0"
        @click="$emit('regenerate-failed')"
        class="px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 text-sm"
      >
        重新生成失败图片
      </button>
    </div>

    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div
        v-for="(image, index) in images"
        :key="index"
        class="relative aspect-[3/4] bg-gray-100 rounded-lg overflow-hidden"
      >
        <!-- Success Image -->
        <img
          v-if="image"
          :src="image"
          :alt="`配图 ${index + 1}`"
          class="w-full h-full object-cover"
        />

        <!-- Failed Image -->
        <div
          v-else
          class="w-full h-full flex flex-col items-center justify-center cursor-pointer hover:bg-gray-200 transition-colors"
          @click="$emit('regenerate-single', index)"
        >
          <div class="text-4xl mb-2">❌</div>
          <p class="text-sm text-gray-600">生成失败</p>
          <p class="text-xs text-gray-500 mt-1">点击重新生成</p>
        </div>

        <!-- Image Number Badge -->
        <div class="absolute top-2 left-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded text-xs">
          {{ index + 1 }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  images: {
    type: Array,
    default: () => []
  }
})

defineEmits(['regenerate-single', 'regenerate-failed'])

const successCount = computed(() => {
  return props.images.filter(img => img !== null).length
})

const failedImages = computed(() => {
  return props.images
    .map((img, index) => img === null ? index : null)
    .filter(index => index !== null)
})
</script>
```

**Step 2: Commit**

```bash
git add .
git commit -m "feat: add image gallery component"
```

---

## Task 7: Result Preview Component

**Files:**
- Create: `frontend/src/components/ResultPreview.vue`

**Step 1: Create ResultPreview component**

Create `frontend/src/components/ResultPreview.vue`:
```vue
<template>
  <div v-if="content" class="w-full bg-white rounded-lg shadow-md p-6">
    <h2 class="text-2xl font-bold mb-4">生成结果</h2>

    <!-- Title -->
    <div class="mb-6">
      <h3 class="text-sm font-medium text-gray-700 mb-2">标题</h3>
      <p class="text-lg font-semibold">{{ content.title }}</p>
    </div>

    <!-- Content -->
    <div class="mb-6">
      <h3 class="text-sm font-medium text-gray-700 mb-2">正文</h3>
      <div class="prose max-w-none whitespace-pre-wrap">
        {{ content.content }}
      </div>
    </div>

    <!-- Images -->
    <div class="mb-6">
      <ImageGallery
        :images="content.images"
        @regenerate-single="handleRegenerateSingle"
        @regenerate-failed="handleRegenerateFailed"
      />
    </div>

    <!-- Actions -->
    <div class="flex gap-3">
      <button
        @click="$emit('save')"
        class="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
      >
        保存
      </button>
      <button
        @click="$emit('edit')"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
      >
        编辑
      </button>
      <button
        @click="$emit('discard')"
        class="px-6 py-3 bg-gray-300 text-gray-700 rounded-lg hover:bg-gray-400"
      >
        放弃
      </button>
    </div>
  </div>
</template>

<script setup>
import ImageGallery from './ImageGallery.vue'

defineProps({
  content: Object
})

const emit = defineEmits(['save', 'edit', 'discard', 'regenerate-single', 'regenerate-failed'])

const handleRegenerateSingle = (index) => {
  emit('regenerate-single', index)
}

const handleRegenerateFailed = () => {
  emit('regenerate-failed')
}
</script>
```

**Step 2: Commit**

```bash
git add .
git commit -m "feat: add result preview component"
```

---

## Task 8: Content Create Page

**Files:**
- Create: `frontend/src/views/ContentCreate.vue`
- Create: `frontend/src/api/content.js`

**Step 1: Create API module**

Create `frontend/src/api/content.js`:
```javascript
// Mock API for MVP - will be replaced with real backend calls
export async function generateContent(topic) {
  // Simulate API call delay
  await sleep(1000)

  return {
    id: `content_${Date.now()}`,
    topic,
    title: `${topic} - 生成的标题`,
    content: `这是关于${topic}的详细内容...\n\n段落1\n\n段落2\n\n段落3`,
    images: Array(12).fill(null),
    status: 'draft',
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString()
  }
}

export async function generateImages(prompts, onProgress) {
  const images = []
  const DELAY_BETWEEN_IMAGES = 3000 // 3 seconds

  for (let i = 0; i < prompts.length; i++) {
    try {
      const image = await generateSingleImage(prompts[i])
      images.push(image)
    } catch (error) {
      images.push(null) // Failed image
    }

    if (onProgress) {
      onProgress(i + 1, prompts.length)
    }

    if (i < prompts.length - 1) {
      await sleep(DELAY_BETWEEN_IMAGES)
    }
  }

  return images
}

async function generateSingleImage(prompt) {
  // Simulate image generation
  await sleep(500)

  // 90% success rate for testing
  if (Math.random() > 0.1) {
    return `https://via.placeholder.com/1080x1440?text=Image+${Math.random().toString(36).substr(2, 9)}`
  } else {
    throw new Error('Image generation failed')
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms))
}

export async function saveContent(content) {
  // Mock save - will be replaced with real backend
  await sleep(500)
  console.log('Saving content:', content)
  return { success: true }
}
```

**Step 2: Create ContentCreate page**

Create `frontend/src/views/ContentCreate.vue`:
```vue
<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <router-link
          to="/"
          class="text-blue-600 hover:text-blue-700 mb-4 inline-block"
        >
          ← 返回首页
        </router-link>
        <h1 class="text-3xl font-bold">创建内容</h1>
      </div>

      <!-- Topic Input -->
      <div class="mb-8">
        <TopicInput
          v-model="topic"
          :loading="isGenerating"
          @submit="handleGenerate"
        />
      </div>

      <!-- Result Preview -->
      <ResultPreview
        v-if="generatedContent"
        :content="generatedContent"
        @save="handleSave"
        @edit="handleEdit"
        @discard="handleDiscard"
        @regenerate-single="handleRegenerateSingle"
        @regenerate-failed="handleRegenerateFailed"
      />

      <!-- Progress Modal -->
      <ProgressModal
        :show="showProgress"
        :title="progressTitle"
        :progress="progress"
        :message="progressMessage"
        :current-step="currentStep"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TopicInput from '../components/TopicInput.vue'
import ResultPreview from '../components/ResultPreview.vue'
import ProgressModal from '../components/ProgressModal.vue'
import { generateContent, generateImages, saveContent } from '../api/content.js'

const router = useRouter()

const topic = ref('')
const isGenerating = ref(false)
const generatedContent = ref(null)

const showProgress = ref(false)
const progressTitle = ref('正在生成内容')
const progress = ref(0)
const progressMessage = ref('请稍候...')
const currentStep = ref('')

async function handleGenerate(topicValue) {
  isGenerating.value = true
  showProgress.value = true
  progress.value = 0
  generatedContent.value = null

  try {
    // Step 1: Generate text content (10%)
    progressMessage.value = '正在生成文案...'
    currentStep.value = '步骤 1/2'
    const content = await generateContent(topicValue)
    progress.value = 10

    // Step 2: Generate images (10% -> 100%)
    progressMessage.value = '正在生成配图...'
    currentStep.value = '步骤 2/2'

    const imagePrompts = Array(12).fill('placeholder prompt')
    const images = await generateImages(imagePrompts, (current, total) => {
      const imageProgress = 10 + (current / total) * 90
      progress.value = Math.round(imageProgress)
      progressMessage.value = `正在生成配图 ${current}/${total}...`
    })

    content.images = images
    generatedContent.value = content
    progress.value = 100
    progressMessage.value = '生成完成！'

    setTimeout(() => {
      showProgress.value = false
    }, 1000)
  } catch (error) {
    console.error('Generation failed:', error)
    progressMessage.value = '生成失败，请重试'
    setTimeout(() => {
      showProgress.value = false
    }, 2000)
  } finally {
    isGenerating.value = false
  }
}

async function handleSave() {
  try {
    await saveContent(generatedContent.value)
    alert('保存成功！')
    router.push('/list')
  } catch (error) {
    console.error('Save failed:', error)
    alert('保存失败，请重试')
  }
}

function handleEdit() {
  // TODO: Implement edit functionality
  alert('编辑功能待实现')
}

function handleDiscard() {
  if (confirm('确定要放弃当前内容吗？')) {
    generatedContent.value = null
    topic.value = ''
  }
}

async function handleRegenerateSingle(index) {
  // TODO: Implement single image regeneration
  console.log('Regenerate image at index:', index)
}

async function handleRegenerateFailed() {
  // TODO: Implement failed images regeneration
  console.log('Regenerate all failed images')
}
</script>
```

**Step 3: Test the page**

Run: `npm run dev`
Expected: Navigate to /create, enter a topic, see progress modal and result preview

**Step 4: Commit**

```bash
git add .
git commit -m "feat: add content create page with mock API"
```

---

## Task 9: Backend API Setup

**Files:**
- Create: `backend/app.py`
- Create: `backend/requirements.txt`
- Create: `backend/.env.example`

**Step 1: Create requirements.txt**

Create `backend/requirements.txt`:
```
flask==3.0.0
flask-cors==4.0.0
python-dotenv==1.0.0
```

**Step 2: Create .env.example**

Create `backend/.env.example`:
```
SKILL_PATH=/Users/dj/Desktop/小静的skills/xiaohongshu-content-generator
```

**Step 3: Create Flask app**

Create `backend/app.py`:
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

SKILL_PATH = os.getenv('SKILL_PATH')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@app.route('/api/generate', methods=['POST'])
def generate_content():
    try:
        data = request.json
        topic = data.get('topic')

        if not topic:
            return jsonify({'error': 'Topic is required'}), 400

        # Call xiaohongshu-content-generator skill
        # This is a placeholder - actual implementation will use Claude Code API
        result = {
            'id': f'content_{int(time.time())}',
            'topic': topic,
            'title': f'{topic} - 生成的标题',
            'content': f'这是关于{topic}的详细内容...',
            'images': [],
            'status': 'draft',
            'createdAt': datetime.now().isoformat(),
            'updatedAt': datetime.now().isoformat()
        }

        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contents', methods=['GET'])
def list_contents():
    # TODO: Read from data/contents directory
    return jsonify([])

@app.route('/api/contents/<content_id>', methods=['GET'])
def get_content(content_id):
    # TODO: Read specific content file
    return jsonify({})

@app.route('/api/contents', methods=['POST'])
def save_content():
    try:
        data = request.json
        # TODO: Save to data/contents directory
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

**Step 4: Install dependencies**

Run: `cd backend && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
Expected: Dependencies installed

**Step 5: Test backend**

Run: `python app.py`
Expected: Server starts on http://localhost:5000

**Step 6: Commit**

```bash
git add .
git commit -m "feat: add Flask backend with basic API endpoints"
```

---

## Task 10: Data Storage Module

**Files:**
- Create: `backend/storage.py`

**Step 1: Create storage module**

Create `backend/storage.py`:
```python
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / 'data'
CONTENTS_DIR = DATA_DIR / 'contents'
IMAGES_DIR = DATA_DIR / 'images'

# Ensure directories exist
CONTENTS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

def save_content(content):
    """Save content to JSON file"""
    content_id = content['id']
    file_path = CONTENTS_DIR / f'{content_id}.json'

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    return content_id

def get_content(content_id):
    """Get content by ID"""
    file_path = CONTENTS_DIR / f'{content_id}.json'

    if not file_path.exists():
        return None

    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def list_contents():
    """List all contents"""
    contents = []

    for file_path in CONTENTS_DIR.glob('*.json'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = json.load(f)
            contents.append(content)

    # Sort by creation date (newest first)
    contents.sort(key=lambda x: x['createdAt'], reverse=True)

    return contents

def delete_content(content_id):
    """Delete content by ID"""
    file_path = CONTENTS_DIR / f'{content_id}.json'

    if file_path.exists():
        file_path.unlink()
        return True

    return False

def save_image(image_data, filename):
    """Save image file"""
    file_path = IMAGES_DIR / filename

    with open(file_path, 'wb') as f:
        f.write(image_data)

    return str(file_path)
```

**Step 2: Update app.py to use storage**

Edit `backend/app.py` to import and use storage module:
```python
from storage import save_content, get_content, list_contents, delete_content
```

**Step 3: Commit**

```bash
git add .
git commit -m "feat: add data storage module for JSON persistence"
```

---

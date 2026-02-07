<template>
  <div class="content-review-panel">
    <div class="review-header">
      <h2>内容预览</h2>
      <p class="review-hint">请确认内容后再生成配图，避免浪费算力</p>
    </div>

    <div class="content-display">
      <div class="content-section">
        <h3>标题</h3>
        <p class="content-title">{{ content.title }}</p>
      </div>

      <div class="content-section">
        <h3>正文</h3>
        <div class="content-body" v-html="formatContent(content.body)"></div>
      </div>

      <div class="content-section" v-if="content.images && content.images.length > 0">
        <h3>配图说明 ({{ content.images.length }}张)</h3>
        <ul class="image-prompts">
          <li v-for="(img, index) in content.images" :key="index">
            {{ index + 1 }}. {{ img.description }}
          </li>
        </ul>
      </div>
    </div>

    <div class="review-actions">
      <button
        class="btn btn-secondary"
        @click="$emit('regenerate')"
        :disabled="loading"
      >
        重新生成内容
      </button>

      <button
        class="btn btn-secondary"
        @click="$emit('edit')"
        :disabled="loading"
      >
        手动编辑
      </button>

      <button
        class="btn btn-primary"
        @click="$emit('confirm')"
        :disabled="loading"
      >
        {{ loading ? '生成中...' : '确认并生成配图' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  content: {
    type: Object,
    required: true
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['regenerate', 'edit', 'confirm'])

function formatContent(body) {
  // Convert line breaks to <br> tags
  return body.replace(/\n/g, '<br>')
}
</script>

<style scoped>
.content-review-panel {
  background: white;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.review-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 2px solid #e5e7eb;
}

.review-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
  margin: 0 0 8px 0;
}

.review-hint {
  color: #6b7280;
  font-size: 14px;
  margin: 0;
}

.content-display {
  margin-bottom: 24px;
}

.content-section {
  margin-bottom: 20px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 6px;
}

.content-section h3 {
  font-size: 16px;
  font-weight: 600;
  color: #374151;
  margin: 0 0 12px 0;
}

.content-title {
  font-size: 18px;
  font-weight: 500;
  color: #111827;
  line-height: 1.6;
  margin: 0;
}

.content-body {
  font-size: 15px;
  color: #374151;
  line-height: 1.8;
  white-space: pre-wrap;
}

.image-prompts {
  list-style: none;
  padding: 0;
  margin: 0;
}

.image-prompts li {
  padding: 8px 0;
  color: #4b5563;
  font-size: 14px;
  border-bottom: 1px solid #e5e7eb;
}

.image-prompts li:last-child {
  border-bottom: none;
}

.review-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover:not(:disabled) {
  background: #e5e7eb;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}
</style>

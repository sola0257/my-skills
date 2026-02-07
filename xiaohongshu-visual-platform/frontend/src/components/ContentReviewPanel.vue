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
</style>

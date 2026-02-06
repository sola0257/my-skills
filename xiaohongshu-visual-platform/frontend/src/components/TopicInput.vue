<template>
  <div class="bg-white rounded-lg shadow p-6">
    <h2 class="text-xl font-semibold mb-4">输入主题</h2>

    <textarea
      v-model="topic"
      placeholder="请输入内容主题，例如：多肉植物养护技巧"
      class="w-full h-32 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
      @keydown.ctrl.enter="handleGenerate"
    ></textarea>

    <div class="mt-4 flex items-center justify-between">
      <p class="text-sm text-gray-500">
        按 Ctrl+Enter 快速生成
      </p>

      <button
        @click="handleGenerate"
        :disabled="!topic.trim() || loading"
        class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
      >
        {{ loading ? '生成中...' : '生成内容' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['generate'])

const topic = ref('')

const handleGenerate = () => {
  if (topic.value.trim() && !props.loading) {
    emit('generate', topic.value.trim())
  }
}
</script>

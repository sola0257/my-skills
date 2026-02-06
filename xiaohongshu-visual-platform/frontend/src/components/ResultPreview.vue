<template>
  <div v-if="content" class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold">{{ content.title }}</h2>
      <span class="px-3 py-1 text-sm rounded-full" :class="statusClass">
        {{ content.status === 'draft' ? '草稿' : '已发布' }}
      </span>
    </div>

    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-2">正文内容</h3>
      <div class="prose max-w-none bg-gray-50 p-4 rounded-lg whitespace-pre-wrap">
        {{ content.content }}
      </div>
    </div>

    <div class="mb-6">
      <h3 class="text-lg font-semibold mb-3">配图 ({{ content.images.length }}张)</h3>
      <div class="grid grid-cols-3 gap-4">
        <div
          v-for="(image, index) in content.images"
          :key="image.id"
          class="relative group"
        >
          <img
            :src="image.url"
            :alt="`Image ${index + 1}`"
            class="w-full h-48 object-cover rounded-lg"
          />
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all rounded-lg flex items-center justify-center">
            <button
              @click="$emit('regenerate-image', index)"
              class="opacity-0 group-hover:opacity-100 px-3 py-1 bg-white text-sm rounded-lg transition-opacity"
            >
              重新生成
            </button>
          </div>
          <p class="mt-1 text-xs text-gray-500 truncate">{{ image.prompt }}</p>
        </div>
      </div>
    </div>

    <div class="flex gap-3">
      <button
        @click="$emit('save')"
        class="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
      >
        保存内容
      </button>
      <button
        @click="$emit('edit')"
        class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        编辑
      </button>
      <button
        @click="$emit('discard')"
        class="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
      >
        放弃
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  content: {
    type: Object,
    default: null
  }
})

defineEmits(['save', 'edit', 'discard', 'regenerate-image'])

const statusClass = computed(() => {
  return props.content?.status === 'published'
    ? 'bg-green-100 text-green-800'
    : 'bg-yellow-100 text-yellow-800'
})
</script>

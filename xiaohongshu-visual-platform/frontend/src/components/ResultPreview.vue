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
          :key="index"
          class="relative group"
        >
          <!-- Image with loading and error states -->
          <div class="relative w-full h-48 bg-gray-100 rounded-lg overflow-hidden">
            <img
              :src="getImageUrl(image)"
              :alt="`Image ${index + 1}`"
              class="w-full h-full object-cover"
              :class="{ 'opacity-0': imageStates[index]?.loading }"
              @load="handleImageLoad(index)"
              @error="handleImageError(index)"
            />

            <!-- Loading state -->
            <div
              v-if="imageStates[index]?.loading"
              class="absolute inset-0 flex items-center justify-center bg-gray-100"
            >
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>

            <!-- Error state -->
            <div
              v-if="imageStates[index]?.error"
              class="absolute inset-0 flex flex-col items-center justify-center bg-gray-100 text-gray-500"
            >
              <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <p class="text-sm">加载失败</p>
            </div>
          </div>

          <!-- Hover overlay with regenerate button -->
          <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all rounded-lg flex items-center justify-center">
            <button
              @click="$emit('regenerate-image', index)"
              class="opacity-0 group-hover:opacity-100 px-3 py-1 bg-white text-sm rounded-lg transition-opacity hover:bg-gray-100"
            >
              重新生成
            </button>
          </div>

          <!-- Image prompt/description -->
          <p v-if="getImagePrompt(image)" class="mt-1 text-xs text-gray-500 truncate">
            {{ getImagePrompt(image) }}
          </p>
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
import { computed, ref, watch } from 'vue'

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

// Image loading states
const imageStates = ref({})

// Initialize image states when content changes
watch(() => props.content?.images, (images) => {
  if (images) {
    imageStates.value = {}
    images.forEach((_, index) => {
      imageStates.value[index] = { loading: true, error: false }
    })
  }
}, { immediate: true })

// Helper function to get image URL (handles both string and object formats)
const getImageUrl = (image) => {
  if (typeof image === 'string') {
    return image
  }
  return image?.url || image?.path || ''
}

// Helper function to get image prompt/description
const getImagePrompt = (image) => {
  if (typeof image === 'object') {
    return image?.prompt || image?.description || ''
  }
  return ''
}

// Handle image load success
const handleImageLoad = (index) => {
  if (imageStates.value[index]) {
    imageStates.value[index].loading = false
    imageStates.value[index].error = false
  }
}

// Handle image load error
const handleImageError = (index) => {
  if (imageStates.value[index]) {
    imageStates.value[index].loading = false
    imageStates.value[index].error = true
  }
}
</script>

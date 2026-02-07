<template>
  <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow overflow-hidden">
    <!-- Thumbnail -->
    <div class="h-48 bg-gray-200 flex items-center justify-center">
      <svg class="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
      </svg>
    </div>

    <!-- Content -->
    <div class="p-4">
      <h3 class="text-lg font-semibold text-gray-800 mb-2 line-clamp-2">
        {{ content.title }}
      </h3>
      <div class="flex items-center justify-between text-sm text-gray-500 mb-3">
        <span>{{ content.date }}</span>
        <span
          class="px-2 py-1 rounded text-xs font-medium"
          :class="statusClass"
        >
          {{ statusText }}
        </span>
      </div>
      <div class="flex gap-2">
        <button
          @click="handleView"
          class="flex-1 px-3 py-2 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 transition-colors text-sm"
        >
          查看
        </button>
        <button
          @click="handleEdit"
          class="flex-1 px-3 py-2 bg-gray-50 text-gray-600 rounded hover:bg-gray-100 transition-colors text-sm"
        >
          编辑
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  content: {
    type: Object,
    required: true
  }
})

const statusClass = computed(() => {
  return props.content.status === 'published'
    ? 'bg-green-100 text-green-800'
    : 'bg-yellow-100 text-yellow-800'
})

const statusText = computed(() => {
  return props.content.status === 'published' ? '已发布' : '草稿'
})

// Navigate to detail view
function handleView() {
  router.push({ name: 'content-detail', params: { id: props.content.id } })
}

// Navigate to edit view (TODO)
function handleEdit() {
  console.log('Edit content:', props.content.id)
  // TODO: Implement edit functionality
}
</script>

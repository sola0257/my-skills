<template>
  <div class="max-w-7xl mx-auto">
    <!-- Filter Buttons -->
    <div class="mb-6 flex gap-3">
      <button
        v-for="filter in filters"
        :key="filter.value"
        @click="currentFilter = filter.value"
        class="px-4 py-2 rounded-lg font-medium transition-colors"
        :class="currentFilter === filter.value
          ? 'bg-blue-600 text-white'
          : 'bg-white text-gray-600 hover:bg-gray-50'"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Content Grid -->
    <div class="grid grid-cols-3 gap-6">
      <ContentCard
        v-for="content in filteredContents"
        :key="content.id"
        :content="content"
      />
    </div>

    <!-- Empty State -->
    <div v-if="filteredContents.length === 0" class="text-center py-12">
      <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-500 text-lg">暂无内容</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import ContentCard from '../components/ContentCard.vue'

const filters = [
  { label: '全部', value: 'all' },
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' }
]

const currentFilter = ref('all')

// Mock data
const contents = ref([
  {
    id: 1,
    title: '多肉植物养护指南：新手必看的5个技巧',
    date: '2024-02-06',
    status: 'published'
  },
  {
    id: 2,
    title: '春季绿植推荐：这些植物最适合办公室',
    date: '2024-02-05',
    status: 'draft'
  },
  {
    id: 3,
    title: '如何让你的绿萝长得更茂盛？',
    date: '2024-02-04',
    status: 'published'
  }
])

const filteredContents = computed(() => {
  if (currentFilter.value === 'all') {
    return contents.value
  }
  return contents.value.filter(c => c.status === currentFilter.value)
})
</script>

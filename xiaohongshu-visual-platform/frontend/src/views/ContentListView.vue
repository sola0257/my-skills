<template>
  <div class="max-w-7xl mx-auto">
    <!-- Filter Buttons -->
    <div class="mb-6 flex gap-3">
      <button
        v-for="filter in filters"
        :key="filter.value"
        @click="handleFilterChange(filter.value)"
        class="px-4 py-2 rounded-lg font-medium transition-colors"
        :class="currentFilter === filter.value
          ? 'bg-blue-600 text-white'
          : 'bg-white text-gray-600 hover:bg-gray-50'"
        :disabled="loading"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      <p class="text-gray-500 mt-4">加载中...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <svg class="w-16 h-16 text-red-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <p class="text-red-500 text-lg mb-4">{{ error }}</p>
      <button
        @click="fetchContents"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        重试
      </button>
    </div>

    <!-- Content Grid -->
    <div v-else-if="filteredContents.length > 0" class="grid grid-cols-3 gap-6">
      <ContentCard
        v-for="content in filteredContents"
        :key="content.id"
        :content="content"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
      <p class="text-gray-500 text-lg">暂无内容</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import ContentCard from '../components/ContentCard.vue'
import { listContents } from '../api/content'

const filters = [
  { label: '全部', value: 'all' },
  { label: '草稿', value: 'draft' },
  { label: '已发布', value: 'published' }
]

const currentFilter = ref('all')
const contents = ref([])
const loading = ref(false)
const error = ref(null)

// Fetch contents from API
async function fetchContents() {
  loading.value = true
  error.value = null

  try {
    const status = currentFilter.value === 'all' ? null : currentFilter.value
    const data = await listContents(status)

    // Transform API response to match component format
    contents.value = data.map(item => ({
      id: item.id,
      title: item.title,
      date: new Date(item.created_at).toLocaleDateString('zh-CN'),
      status: item.status
    }))
  } catch (err) {
    error.value = err.message || '加载内容失败'
    console.error('Failed to fetch contents:', err)
  } finally {
    loading.value = false
  }
}

// Fetch on mount
onMounted(() => {
  fetchContents()
})

// Refetch when filter changes
function handleFilterChange(filterValue) {
  currentFilter.value = filterValue
  fetchContents()
}

const filteredContents = computed(() => {
  return contents.value
})
</script>

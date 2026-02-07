<template>
  <div class="max-w-4xl mx-auto">
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
        @click="fetchContent"
        class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
      >
        重试
      </button>
    </div>

    <!-- Content Detail -->
    <div v-else-if="content" class="bg-white rounded-lg shadow-md p-6">
      <!-- Header -->
      <div class="mb-6">
        <div class="flex items-center justify-between mb-4">
          <button
            @click="$router.back()"
            class="flex items-center text-gray-600 hover:text-gray-800 transition-colors"
          >
            <svg class="w-5 h-5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
            </svg>
            返回
          </button>
          <span
            class="px-3 py-1 rounded text-sm font-medium"
            :class="statusClass"
          >
            {{ statusText }}
          </span>
        </div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2">{{ content.title }}</h1>
        <div class="flex items-center text-sm text-gray-500">
          <span>创建时间：{{ formatDate(content.created_at) }}</span>
          <span class="mx-2">•</span>
          <span>更新时间：{{ formatDate(content.updated_at) }}</span>
        </div>
      </div>

      <!-- Content -->
      <div class="mb-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-3">正文内容</h2>
        <div class="prose max-w-none text-gray-700 whitespace-pre-wrap">
          {{ content.content }}
        </div>
      </div>

      <!-- Images -->
      <div v-if="content.images && content.images.length > 0" class="mb-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-3">配图（{{ content.images.length }}张）</h2>
        <div class="grid grid-cols-3 gap-4">
          <div
            v-for="(image, index) in content.images"
            :key="index"
            class="relative aspect-[3/4] bg-gray-100 rounded-lg overflow-hidden"
          >
            <img
              v-if="imageLoaded[index]"
              :src="getImageUrl(image)"
              :alt="`配图 ${index + 1}`"
              class="w-full h-full object-cover"
              @error="handleImageError(index)"
            />
            <div
              v-else-if="imageError[index]"
              class="absolute inset-0 flex flex-col items-center justify-center text-gray-400"
            >
              <svg class="w-12 h-12 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span class="text-sm">加载失败</span>
            </div>
            <div
              v-else
              class="absolute inset-0 flex items-center justify-center"
            >
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-3 pt-6 border-t">
        <button
          @click="handleEdit"
          class="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          编辑
        </button>
        <button
          @click="handleDelete"
          class="px-4 py-2 bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition-colors"
        >
          删除
        </button>
      </div>
    </div>

    <!-- Delete Confirmation Dialog -->
    <div
      v-if="showDeleteDialog"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="cancelDelete"
    >
      <div class="bg-white rounded-lg p-6 max-w-md w-full mx-4">
        <h3 class="text-xl font-semibold text-gray-800 mb-4">确认删除</h3>
        <p class="text-gray-600 mb-6">
          确定要删除这篇内容吗？此操作无法撤销。
        </p>
        <div class="flex gap-3">
          <button
            @click="cancelDelete"
            :disabled="deleting"
            class="flex-1 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors disabled:opacity-50"
          >
            取消
          </button>
          <button
            @click="confirmDelete"
            :disabled="deleting"
            class="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50 flex items-center justify-center"
          >
            <span v-if="!deleting">确认删除</span>
            <div v-else class="flex items-center">
              <div class="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
              删除中...
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getContent, deleteContent } from '../api/content'

const route = useRoute()
const router = useRouter()

const content = ref(null)
const loading = ref(false)
const error = ref(null)
const imageLoaded = reactive({})
const imageError = reactive({})
const showDeleteDialog = ref(false)
const deleting = ref(false)

// Fetch content by ID
async function fetchContent() {
  loading.value = true
  error.value = null

  try {
    const id = route.params.id
    const data = await getContent(id)
    content.value = data

    // Initialize image loading states
    if (data.images && data.images.length > 0) {
      data.images.forEach((_, index) => {
        imageLoaded[index] = false
        imageError[index] = false
        // Preload images
        const img = new Image()
        img.onload = () => {
          imageLoaded[index] = true
        }
        img.onerror = () => {
          imageError[index] = true
        }
        img.src = getImageUrl(data.images[index])
      })
    }
  } catch (err) {
    error.value = err.message || '加载内容失败'
    console.error('Failed to fetch content:', err)
  } finally {
    loading.value = false
  }
}

// Get image URL from various formats
function getImageUrl(image) {
  if (typeof image === 'string') return image
  return image?.url || image?.path || ''
}

// Handle image load error
function handleImageError(index) {
  imageError[index] = true
}

// Handle edit action
function handleEdit() {
  // TODO: Navigate to edit view
  console.log('Edit content:', content.value.id)
}

// Handle delete action
function handleDelete() {
  showDeleteDialog.value = true
}

// Confirm delete
async function confirmDelete() {
  deleting.value = true

  try {
    await deleteContent(content.value.id)
    // Navigate back to list after successful delete
    router.push({ name: 'list' })
  } catch (err) {
    error.value = err.message || '删除失败'
    console.error('Failed to delete content:', err)
    showDeleteDialog.value = false
  } finally {
    deleting.value = false
  }
}

// Cancel delete
function cancelDelete() {
  showDeleteDialog.value = false
}

// Status display
const statusClass = computed(() => {
  return content.value?.status === 'published'
    ? 'bg-green-100 text-green-800'
    : 'bg-yellow-100 text-yellow-800'
})

const statusText = computed(() => {
  return content.value?.status === 'published' ? '已发布' : '草稿'
})

// Format date
function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Fetch on mount
onMounted(() => {
  fetchContent()
})
</script>

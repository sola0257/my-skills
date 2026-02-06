<template>
  <div
    v-if="show"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
    @click.self="$emit('close')"
  >
    <div class="bg-white rounded-lg shadow-xl p-8 max-w-md w-full mx-4">
      <h3 class="text-xl font-semibold mb-4">{{ title }}</h3>

      <div class="mb-4">
        <div class="flex justify-between text-sm text-gray-600 mb-2">
          <span>{{ currentStep }}</span>
          <span>{{ progress }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="bg-blue-600 h-2 rounded-full transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
      </div>

      <p class="text-gray-600 text-sm">{{ message }}</p>

      <button
        v-if="canClose"
        @click="$emit('close')"
        class="mt-6 w-full px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
      >
        关闭
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: '生成中'
  },
  currentStep: {
    type: String,
    default: ''
  },
  message: {
    type: String,
    default: ''
  },
  progress: {
    type: Number,
    default: 0
  },
  canClose: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close'])
</script>

<template>
  <div class="max-w-6xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8">创建内容</h1>

    <!-- Topic Input Section -->
    <TopicInput
      v-if="!result"
      @generate="handleGenerate"
    />

    <!-- Result Preview Section -->
    <ResultPreview
      v-if="result"
      :content="result"
      @save="handleSave"
      @edit="handleEdit"
      @discard="handleDiscard"
      @regenerate-single="handleRegenerateSingle"
    />

    <!-- Progress Modal -->
    <ProgressModal
      :show="showProgress"
      :title="progressTitle"
      :message="progressMessage"
      :progress="progress"
      :total="progressTotal"
      @close="showProgress = false"
    />
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TopicInput from '../components/TopicInput.vue'
import ResultPreview from '../components/ResultPreview.vue'
import ProgressModal from '../components/ProgressModal.vue'
import { generateContent, generateImages, saveContent } from '../api/content.js'

export default {
  name: 'CreateView',
  components: {
    TopicInput,
    ResultPreview,
    ProgressModal
  },
  setup() {
    const router = useRouter()
    const result = ref(null)
    const showProgress = ref(false)
    const progressTitle = ref('')
    const progressMessage = ref('')
    const progress = ref(0)
    const progressTotal = ref(0)

    const handleGenerate = async (topic) => {
      try {
        // Show progress modal
        showProgress.value = true
        progressTitle.value = '正在生成内容'
        progressMessage.value = '正在生成文案...'
        progress.value = 0
        progressTotal.value = 2

        // Step 1: Generate content
        const content = await generateContent(topic)
        progress.value = 1
        progressMessage.value = '正在生成配图...'

        // Step 2: Generate images
        const imagePrompts = content.images.map(img => img.prompt)
        const images = await generateImages(imagePrompts, (current, total) => {
          progressMessage.value = `正在生成配图 ${current}/${total}...`
        })

        // Update content with generated images
        content.images = images
        progress.value = 2

        // Hide progress and show result
        showProgress.value = false
        result.value = content

      } catch (error) {
        console.error('生成失败:', error)
        showProgress.value = false
        alert('生成失败，请重试')
      }
    }

    const handleSave = async () => {
      try {
        showProgress.value = true
        progressTitle.value = '正在保存'
        progressMessage.value = '保存中...'

        await saveContent(result.value)

        showProgress.value = false
        alert('保存成功！')
        router.push('/list')

      } catch (error) {
        console.error('保存失败:', error)
        showProgress.value = false
        alert('保存失败，请重试')
      }
    }

    const handleEdit = () => {
      // For MVP, just allow re-editing the topic
      result.value = null
    }

    const handleDiscard = () => {
      if (confirm('确定要丢弃当前内容吗？')) {
        result.value = null
      }
    }

    const handleRegenerateSingle = async (index) => {
      try {
        showProgress.value = true
        progressTitle.value = '重新生成'
        progressMessage.value = `正在重新生成第 ${index + 1} 张图片...`

        const prompt = result.value.images[index].prompt
        const newImages = await generateImages([prompt])

        result.value.images[index] = newImages[0]
        showProgress.value = false

      } catch (error) {
        console.error('重新生成失败:', error)
        showProgress.value = false
        alert('重新生成失败，请重试')
      }
    }

    return {
      result,
      showProgress,
      progressTitle,
      progressMessage,
      progress,
      progressTotal,
      handleGenerate,
      handleSave,
      handleEdit,
      handleDiscard,
      handleRegenerateSingle
    }
  }
}
</script>

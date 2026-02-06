// Mock API for content generation
// This will be replaced with real API calls later

/**
 * Generate content based on topic
 * @param {string} topic - The topic to generate content for
 * @returns {Promise<Object>} Generated content with title, content, and images
 */
export async function generateContent(topic) {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 2000))

  return {
    id: Date.now().toString(),
    topic,
    title: `${topic}的完整指南`,
    content: `这是关于${topic}的详细内容。\n\n## 第一部分\n这里是第一部分的内容...\n\n## 第二部分\n这里是第二部分的内容...`,
    images: Array(12).fill(null).map((_, i) => ({
      id: `img-${i}`,
      url: `https://via.placeholder.com/400x533?text=Image+${i + 1}`,
      prompt: `Image ${i + 1} for ${topic}`
    })),
    status: 'draft',
    createdAt: new Date().toISOString()
  }
}

/**
 * Generate images based on prompts with progress callback
 * @param {Array<string>} prompts - Array of image prompts
 * @param {Function} onProgress - Progress callback (current, total)
 * @returns {Promise<Array<Object>>} Generated images
 */
export async function generateImages(prompts, onProgress) {
  const images = []

  for (let i = 0; i < prompts.length; i++) {
    // Simulate image generation delay
    await new Promise(resolve => setTimeout(resolve, 500))

    images.push({
      id: `img-${i}`,
      url: `https://via.placeholder.com/400x533?text=Image+${i + 1}`,
      prompt: prompts[i]
    })

    if (onProgress) {
      onProgress(i + 1, prompts.length)
    }
  }

  return images
}

/**
 * Save content to storage
 * @param {Object} content - Content object to save
 * @returns {Promise<Object>} Saved content with id
 */
export async function saveContent(content) {
  console.log('Saving content:', content)

  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500))

  return {
    ...content,
    id: content.id || Date.now().toString(),
    savedAt: new Date().toISOString()
  }
}

/**
 * List all contents
 * @returns {Promise<Array<Object>>} Array of content objects
 */
export async function listContents() {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 300))

  return [
    {
      id: '1',
      topic: '多肉植物养护',
      title: '多肉植物养护完全指南',
      thumbnail: 'https://via.placeholder.com/400x533?text=Thumbnail+1',
      status: 'published',
      createdAt: '2024-01-15T10:00:00Z'
    },
    {
      id: '2',
      topic: '室内绿植推荐',
      title: '10种适合室内养护的绿植',
      thumbnail: 'https://via.placeholder.com/400x533?text=Thumbnail+2',
      status: 'draft',
      createdAt: '2024-01-16T14:30:00Z'
    },
    {
      id: '3',
      topic: '春季园艺',
      title: '春季园艺必做的5件事',
      thumbnail: 'https://via.placeholder.com/400x533?text=Thumbnail+3',
      status: 'published',
      createdAt: '2024-01-17T09:15:00Z'
    }
  ]
}

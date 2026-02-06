// API client for content generation
// Connects to backend API at http://localhost:5001

const API_BASE = '/api'

/**
 * Handle API response
 * @param {Response} response - Fetch response
 * @returns {Promise<Object>} Parsed JSON response
 */
async function handleResponse(response) {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Unknown error' }))
    throw new Error(error.error || `HTTP ${response.status}: ${response.statusText}`)
  }
  return response.json()
}

/**
 * Generate content based on topic
 * @param {string} topic - The topic to generate content for
 * @returns {Promise<Object>} Generated content with title, content, and images
 */
export async function generateContent(topic) {
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ topic })
  })

  return handleResponse(response)
}

/**
 * Generate images based on prompts with progress callback
 * @param {Array<string>} prompts - Array of image prompts
 * @param {Function} onProgress - Progress callback (current, total)
 * @returns {Promise<Array<Object>>} Generated images
 */
export async function generateImages(prompts, onProgress) {
  // For now, this is still mock since we haven't implemented image generation yet
  // This will be replaced in Task 13
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
  const response = await fetch(`${API_BASE}/contents`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(content)
  })

  return handleResponse(response)
}

/**
 * List all contents
 * @param {string} status - Optional status filter ('draft', 'published')
 * @returns {Promise<Array<Object>>} Array of content objects
 */
export async function listContents(status = null) {
  const url = status ? `${API_BASE}/contents?status=${status}` : `${API_BASE}/contents`
  const response = await fetch(url)

  return handleResponse(response)
}

/**
 * Get content by ID
 * @param {string} id - Content ID
 * @returns {Promise<Object>} Content object
 */
export async function getContent(id) {
  const response = await fetch(`${API_BASE}/contents/${id}`)

  return handleResponse(response)
}

/**
 * Update content
 * @param {string} id - Content ID
 * @param {Object} updates - Fields to update
 * @returns {Promise<Object>} Updated content
 */
export async function updateContent(id, updates) {
  const response = await fetch(`${API_BASE}/contents/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  })

  return handleResponse(response)
}

/**
 * Delete content
 * @param {string} id - Content ID
 * @returns {Promise<Object>} Success message
 */
export async function deleteContent(id) {
  const response = await fetch(`${API_BASE}/contents/${id}`, {
    method: 'DELETE'
  })

  return handleResponse(response)
}

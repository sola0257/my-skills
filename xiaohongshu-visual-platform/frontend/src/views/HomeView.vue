<template>
  <div class="max-w-6xl mx-auto">
    <!-- Welcome Section -->
    <div class="bg-white rounded-lg shadow-md p-8 mb-8">
      <h1 class="text-4xl font-bold text-gray-800 mb-4">小红书内容管理平台</h1>
      <p class="text-lg text-gray-600">
        快速生成高质量的小红书内容，可视化管理您的创作，本地安全存储
      </p>
    </div>

    <!-- Feature Cards -->
    <div class="grid grid-cols-3 gap-6">
      <!-- Card 1: 快速生成 -->
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">快速生成</h3>
        <p class="text-gray-600 mb-4">
          输入主题，AI 自动生成标题、正文和配图，节省创作时间
        </p>
        <ul class="text-sm text-gray-500 space-y-1">
          <li>• 智能标题生成</li>
          <li>• 自动配图建议</li>
          <li>• 多种风格选择</li>
        </ul>
      </div>

      <!-- Card 2: 可视化管理 -->
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">可视化管理</h3>
        <p class="text-gray-600 mb-4">
          直观的界面管理所有内容，轻松编辑、预览和发布
        </p>
        <ul class="text-sm text-gray-500 space-y-1">
          <li>• 内容列表视图</li>
          <li>• 实时预览效果</li>
          <li>• 状态管理</li>
        </ul>
      </div>

      <!-- Card 3: 本地存储 -->
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
        <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
          <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01" />
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">本地存储</h3>
        <p class="text-gray-600 mb-4">
          所有数据保存在本地，安全可靠，随时访问
        </p>
        <ul class="text-sm text-gray-500 space-y-1">
          <li>• 数据本地化</li>
          <li>• 隐私保护</li>
          <li>• 离线可用</li>
        </ul>
      </div>
    </div>

    <!-- CTA Button -->
    <div class="mt-8 text-center">
      <router-link
        to="/create"
        class="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
      >
        开始创建
      </router-link>
    </div>
  </div>
</template>

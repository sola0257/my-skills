<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-gray-800 text-white flex flex-col">
      <div class="p-4 border-b border-gray-700">
        <h1 class="text-xl font-bold">小红书内容管理</h1>
      </div>
      <nav class="flex-1 p-4">
        <router-link
          to="/"
          class="block py-2 px-4 rounded hover:bg-gray-700 mb-2"
          active-class="bg-gray-700"
        >
          首页
        </router-link>
        <router-link
          to="/create"
          class="block py-2 px-4 rounded hover:bg-gray-700 mb-2"
          active-class="bg-gray-700"
        >
          创建内容
        </router-link>
        <router-link
          to="/list"
          class="block py-2 px-4 rounded hover:bg-gray-700 mb-2"
          active-class="bg-gray-700"
        >
          内容列表
        </router-link>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-auto">
      <header class="bg-white shadow-sm p-4">
        <h2 class="text-2xl font-semibold text-gray-800">{{ pageTitle }}</h2>
      </header>
      <div class="p-6">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const pageTitle = computed(() => {
  const titles = {
    '/': '欢迎',
    '/create': '创建内容',
    '/list': '内容列表'
  }
  return titles[route.path] || '小红书内容管理'
})
</script>

import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/create',
    name: 'create',
    component: () => import('../views/CreateView.vue')
  },
  {
    path: '/list',
    name: 'list',
    component: () => import('../views/ContentListView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

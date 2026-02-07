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
  },
  {
    path: '/content/:id',
    name: 'content-detail',
    component: () => import('../views/ContentDetailView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

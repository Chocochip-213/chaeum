import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  scrollBehavior() {
    return { top: 0 }
  },

  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { layout: 'empty' },
    },
    {
      path: '/signup',
      name: 'signup',
      component: () => import('@/views/SignupView.vue'),
      meta: { layout: 'empty' },
    },
    {
      path: '/find-password',
      name: 'find-password',
      component: () => import('@/views/FindPasswordView.vue'),
      meta: { layout: 'empty' },
    },
    {
      path: '/reset-password/:uidb64/:token',
      name: 'reset-password',
      component: () => import('@/views/ResetPassword.vue'),
      props: true,
      meta: { layout: 'empty' },
    },
    {
      path: '/books',
      name: 'book-list',
      component: () => import('@/views/BookListView.vue'),
    },
    {
      path: '/books/:isbn',
      name: 'book-detail',
      component: () => import('@/views/BookDetailView.vue'),
      props: true,
    },
    {
      path: '/analysis',
      name: 'analysis',
      component: () => import('@/views/AnalysisView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/analysis/result/:id',
      name: 'analysis-result',
      component: () => import('@/views/AnalysisResultView.vue'),
      meta: { requiresAuth: true },
      props: true,
    },
    {
      path: '/community/write',
      name: 'community-write',
      component: () => import('@/views/CommunityWriteView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/community',
      name: 'community',
      component: () => import('@/views/CommunityView.vue'),
    },
    {
      path: '/community/:id',
      name: 'community-detail',
      component: () => import('@/views/CommunityDetailView.vue'),
      props: true,
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/MyPageView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token')

  if (to.meta.requiresAuth && !isAuthenticated) {
    alert('로그인이 필요한 서비스입니다.')
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页', requiresAuth: true }
  },
  {
    path: '/assessment',
    name: 'CareerAssessment',
    component: () => import('@/views/CareerAssessment.vue'),
    meta: { title: '职业测评', requiresAuth: true }
  },
  {
    path: '/interview',
    name: 'MockInterview',
    component: () => import('@/views/MockInterview.vue'),
    meta: { title: '模拟面试', requiresAuth: true }
  },
  {
    path: '/interview/session',
    name: 'InterviewSession',
    component: () => import('@/views/InterviewSession.vue'),
    meta: { title: '面试进行中', requiresAuth: true }
  },
  {
    path: '/interview/result/:id',
    name: 'InterviewResult',
    component: () => import('@/views/InterviewResult.vue'),
    meta: { title: '面试结果', requiresAuth: true }
  },
  {
    path: '/jobs',
    name: 'JobExplore',
    redirect: '/jobs/list',
    meta: { title: '岗位探索', requiresAuth: true },
    children: [
      {
        path: 'list',
        name: 'JobList',
        component: () => import('@/views/JobList.vue'),
        meta: { title: '岗位列表', requiresAuth: true }
      },
      {
        path: 'graph',
        name: 'JobGraph',
        component: () => import('@/views/JobGraph.vue'),
        meta: { title: '岗位图谱', requiresAuth: true }
      }
    ]
  },
  {
    path: '/student-profile',
    name: 'StudentProfile',
    component: () => import('@/views/StudentProfile.vue'),
    meta: { title: '学生画像', requiresAuth: true }
  },
  {
    path: '/plan',
    name: 'CareerPlan',
    component: () => import('@/views/CareerPlan.vue'),
    meta: { title: '职业规划', requiresAuth: true }
  },
  {
    path: '/reports',
    name: 'ReportCenter',
    component: () => import('@/views/ReportCenter.vue'),
    meta: { title: '报告中心', requiresAuth: true }
  },
  {
    path: '/ai',
    name: 'AIAssistant',
    component: () => import('@/views/AIAssistant.vue'),
    meta: { title: 'AI助手', requiresAuth: true }
  },
  {
    path: '/settings',
    name: 'UserCenter',
    component: () => import('@/views/UserCenter.vue'),
    meta: { title: '个人中心', requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStorage = localStorage.getItem('auth-storage')
  let isAuthenticated = false

  if (authStorage) {
    try {
      const authData = JSON.parse(authStorage)
      const user = authData?.user
      const token = authData?.token
      isAuthenticated = !!(user && token)
    } catch (e) {
      console.error('解析认证信息失败:', e)
    }
  }

  if (to.meta.title) {
    document.title = `${to.meta.title} | 职业规划智能体`
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  if (to.path === '/login' && isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router

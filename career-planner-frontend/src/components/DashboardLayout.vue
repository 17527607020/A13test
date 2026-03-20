<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <!-- Logo区域 - 可点击跳转首页 -->
      <router-link to="/" class="sidebar-header">
        <el-icon class="logo-icon">
          <Opportunity />
        </el-icon>
        <h1 class="logo-text">职业规划智能体</h1>
      </router-link>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <template v-for="item in navItems" :key="item.id">
          <!-- 有子菜单的项 -->
          <div v-if="item.children" class="nav-group">
            <div class="nav-item" :class="{ active: isGroupActive(item) }" @click="toggleGroup(item.id)">
              <el-icon class="nav-icon">
                <component :is="item.icon" />
              </el-icon>
              <span class="nav-label">{{ item.label }}</span>
              <el-icon class="arrow-icon" :class="{ expanded: expandedGroups.includes(item.id) }">
                <ArrowDown />
              </el-icon>
            </div>
            <transition name="slide">
              <div v-show="expandedGroups.includes(item.id)" class="nav-children">
                <router-link v-for="child in item.children" :key="child.id" :to="child.path" class="nav-item child-item"
                  :class="{ active: isActive(child.path) }">
                  <el-icon class="nav-icon child-icon">
                    <component :is="child.icon" />
                  </el-icon>
                  <span class="nav-label">{{ child.label }}</span>
                </router-link>
              </div>
            </transition>
          </div>

          <!-- 无子菜单的项 -->
          <router-link v-else :to="item.path!" class="nav-item" :class="{ active: isActive(item.path!) }">
            <el-icon class="nav-icon">
              <component :is="item.icon" />
            </el-icon>
            <span class="nav-label">{{ item.label }}</span>
          </router-link>
        </template>
      </nav>

      <!-- 用户信息卡片 -->
      <div class="user-card">
        <div class="user-card-content">
          <el-avatar :size="48" :src="avatarUrl" class="user-avatar" />
          <div class="user-details">
            <span class="user-name">{{ username }}</span>
            <span class="user-role">{{ roleLabel }}</span>
          </div>
        </div>
      </div>

      <!-- 退出登录 -->
      <div class="sidebar-footer">
        <el-button type="danger" plain @click="handleLogout">
          <el-icon>
            <SwitchButton />
          </el-icon>
          <span>退出登录</span>
        </el-button>
      </div>
    </aside>

    <main class="main-content">
      <header class="header">
        <div class="header-left">
          <!-- 面包屑导航 -->
          <nav class="breadcrumb">
            <router-link to="/" class="breadcrumb-item home">
              <el-icon>
                <HomeFilled />
              </el-icon>
              <span>首页</span>
            </router-link>
            <template v-if="breadcrumbItems.length > 0">
              <span class="breadcrumb-separator">/</span>
              <template v-for="(item, index) in breadcrumbItems" :key="index">
                <span class="breadcrumb-item" :class="{ active: index === breadcrumbItems.length - 1 }">
                  {{ item }}
                </span>
                <span v-if="index < breadcrumbItems.length - 1" class="breadcrumb-separator">/</span>
              </template>
            </template>
          </nav>
        </div>
        <div class="header-right">
          <el-input v-model="searchKeyword" placeholder="全局搜索..." class="search-input" clearable />
          <div class="user-info">
            <el-avatar :size="32" :src="avatarUrl" />
            <span class="username">{{ username }}</span>
          </div>
        </div>
      </header>

      <div class="page-content">
        <slot></slot>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import {
  Opportunity,
  HomeFilled,
  Briefcase,
  Share,
  User,
  Document,
  ChatDotRound,
  Setting,
  ArrowDown,
  SwitchButton,
  List,
  Connection,
  EditPen,
  Microphone
} from '@element-plus/icons-vue'

interface NavChild {
  id: string
  label: string
  path: string
  icon: any
}

interface NavItem {
  id: string
  label: string
  path?: string
  icon: any
  children?: NavChild[]
}

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const searchKeyword = ref('')
const expandedGroups = ref<string[]>([])

const navItems: NavItem[] = [
  { id: 'home', label: '首页', path: '/', icon: HomeFilled },
  { id: 'assessment', label: '职业测评', path: '/assessment', icon: EditPen },
  { id: 'interview', label: '模拟面试', path: '/interview', icon: Microphone },
  {
    id: 'jobs',
    label: '岗位探索',
    icon: Briefcase,
    children: [
      { id: 'jobs-list', label: '岗位列表', path: '/jobs/list', icon: List },
      { id: 'jobs-graph', label: '岗位图谱', path: '/jobs/graph', icon: Connection }
    ]
  },
  { id: 'profile', label: '学生画像', path: '/student-profile', icon: User },
  { id: 'plan', label: '职业规划', path: '/plan', icon: Share },
  { id: 'reports', label: '报告中心', path: '/reports', icon: Document },
  { id: 'ai', label: 'AI助手', path: '/ai', icon: ChatDotRound },
  { id: 'settings', label: '个人中心', path: '/settings', icon: Setting }
]

const username = computed(() => userStore.user?.username || '用户')

const roleLabel = computed(() => {
  const roleMap: Record<string, string> = {
    student: '学生',
    mentor: '导师',
    admin: '管理员'
  }
  return roleMap[userStore.user?.role || 'student'] || '学生'
})

const avatarUrl = computed(() => {
  return `https://api.dicebear.com/7.x/avataaars/svg?seed=${userStore.user?.username || 'user'}`
})

// 面包屑导航
const breadcrumbItems = computed(() => {
  const path = route.path
  const items: string[] = []

  // 首页时不显示额外面包屑
  if (path === '/') {
    return items
  }

  // 遍历导航项，找到匹配的路径
  for (const item of navItems) {
    if (item.path === path) {
      items.push(item.label)
      break
    }
    if (item.children) {
      const child = item.children.find(c => c.path === path)
      if (child) {
        items.push(item.label)
        items.push(child.label)
        break
      }
    }
  }

  return items
})

const isActive = (path: string) => {
  return route.path === path
}

const isGroupActive = (item: NavItem) => {
  if (item.children) {
    return item.children.some(child => route.path === child.path)
  }
  return false
}

const toggleGroup = (id: string) => {
  const index = expandedGroups.value.indexOf(id)
  if (index > -1) {
    expandedGroups.value.splice(index, 1)
  } else {
    expandedGroups.value.push(id)
  }
}

watch(
  () => route.path,
  (path) => {
    navItems.forEach(item => {
      if (item.children && item.children.some(child => path === child.path)) {
        if (!expandedGroups.value.includes(item.id)) {
          expandedGroups.value.push(item.id)
        }
      }
    })
  },
  { immediate: true }
)

const handleLogout = () => {
  userStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
// 主布局容器
.dashboard-layout {
  display: flex;
  min-height: 100vh;
  background: #f0f2f5;
  overflow: hidden;
}

// 侧边栏
.sidebar {
  width: 240px;
  background: #fff;
  display: flex;
  flex-direction: column;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  z-index: 100;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.06);
}

// Logo区域
.sidebar-header {
  padding: 1.25rem 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-bottom: 1px solid #ebeef5;
  text-decoration: none;
  transition: background 0.2s ease;

  &:hover {
    background: #f5f7fa;
  }

  .logo-icon {
    font-size: 1.75rem;
    color: #409eff;
  }

  .logo-text {
    font-size: 1.1rem;
    font-weight: 600;
    color: #303133;
    margin: 0;
    letter-spacing: 0.5px;
  }
}

// 导航菜单
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 0.75rem 0;

  &::-webkit-scrollbar {
    width: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: #dcdfe6;
    border-radius: 2px;
  }
}

// 导航分组
.nav-group {
  .nav-item {
    cursor: pointer;
  }
}

// 导航项
.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.25rem;
  color: #606266;
  text-decoration: none;
  transition: all 0.25s ease;
  margin: 0.25rem 0.75rem;
  border-radius: 8px;
  position: relative;

  .nav-icon {
    font-size: 1.125rem;
    flex-shrink: 0;
  }

  .nav-label {
    flex: 1;
    font-size: 0.9rem;
  }

  .arrow-icon {
    font-size: 0.75rem;
    color: #909399;
    transition: transform 0.3s ease;

    &.expanded {
      transform: rotate(180deg);
    }
  }

  &:hover {
    background: #ecf5ff;
    color: #409eff;
  }

  &.active {
    background: linear-gradient(90deg, #409eff 0%, #337ecc 100%);
    color: #fff;
    box-shadow: 0 4px 12px rgba(64, 158, 255, 0.25);

    .nav-icon {
      color: #fff;
    }

    .arrow-icon {
      color: rgba(255, 255, 255, 0.8);
    }
  }
}

// 子菜单
.nav-children {
  overflow: hidden;
  padding-left: 1.5rem;

  .child-item {
    padding-left: 1.75rem;
    font-size: 0.85rem;
    margin: 0.125rem 0.75rem 0.125rem 0;

    .child-icon {
      font-size: 1rem;
    }
  }
}

// 展开动画
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-height: 0;
}

.slide-enter-to,
.slide-leave-from {
  opacity: 1;
  max-height: 200px;
}

// 用户信息卡片
.user-card {
  padding: 1rem;
  margin: 0.5rem 0.75rem;
  background: #f5f7fa;
  border-radius: 12px;
  border: 1px solid #ebeef5;

  .user-card-content {
    display: flex;
    align-items: center;
    gap: 0.875rem;
  }

  .user-avatar {
    border: 2px solid #409eff;
    flex-shrink: 0;
    background: #fff;
  }

  .user-details {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    overflow: hidden;

    .user-name {
      font-size: 0.95rem;
      font-weight: 500;
      color: #303133;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .user-role {
      font-size: 0.75rem;
      color: #409eff;
      background: #ecf5ff;
      padding: 0.125rem 0.5rem;
      border-radius: 4px;
      width: fit-content;
    }
  }
}

// 退出登录
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #ebeef5;

  :deep(.el-button) {
    width: 100%;
    border-radius: 8px;
    font-weight: 500;

    .el-icon {
      margin-right: 0.5rem;
    }
  }
}

// 主内容区
.main-content {
  flex: 1;
  margin-left: 240px;
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
}

// 顶部栏
.header {
  background: #fff;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
}

// 面包屑导航
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;

  .breadcrumb-item {
    color: #606266;
    transition: color 0.2s ease;

    &.home {
      display: flex;
      align-items: center;
      gap: 0.25rem;
      text-decoration: none;
      color: #409eff;
      font-weight: 500;

      &:hover {
        color: #337ecc;
      }

      .el-icon {
        font-size: 1rem;
      }
    }

    &.active {
      color: #303133;
      font-weight: 500;
    }
  }

  .breadcrumb-separator {
    color: #c0c4cc;
    margin: 0 0.25rem;
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;

  .search-input {
    width: 280px;
  }

  .user-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;

    .username {
      color: #303133;
      font-weight: 500;
    }
  }
}

// 页面内容
.page-content {
  flex: 1;
  padding: 1.5rem;
  overflow-y: auto;
  background: #f0f2f5;
}
</style>

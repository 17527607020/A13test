<template>
  <div class="home-page" v-loading="loading">
    <!-- 欢迎卡片 -->
    <div class="welcome-card">
      <div class="welcome-content">
        <div class="welcome-left">
          <div class="welcome-date">{{ currentDate }}</div>
          <div class="welcome-text">
            {{ greeting }}，<span class="username">{{ homeData?.username || '用户' }}</span>！
          </div>
          <div class="welcome-message">让我们继续你的职业规划之旅</div>
          <el-button type="primary" class="welcome-btn" @click="$router.push('/plan')">
            开始规划
          </el-button>
        </div>
        <div class="welcome-right">
          <!-- SVG装饰插图 -->
          <svg class="welcome-illustration" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg">
            <circle cx="320" cy="100" r="80" fill="rgba(255,255,255,0.1)" />
            <circle cx="280" cy="60" r="40" fill="rgba(255,255,255,0.08)" />
            <ellipse cx="200" cy="185" rx="60" ry="10" fill="rgba(0,0,0,0.1)" />
            <path d="M170 120 Q165 150 175 180 L225 180 Q235 150 230 120 Z" fill="#fff" opacity="0.95" />
            <circle cx="200" cy="85" r="35" fill="#FFE4C4" />
            <path d="M165 75 Q165 55 185 50 Q200 45 215 50 Q235 55 235 75 Q235 65 220 60 Q200 55 180 60 Q165 65 165 75"
              fill="#4A3728" />
            <circle cx="188" cy="82" r="4" fill="#333" />
            <circle cx="212" cy="82" r="4" fill="#333" />
            <path d="M190 95 Q200 102 210 95" stroke="#333" stroke-width="2" fill="none" stroke-linecap="round" />
            <path d="M230 130 Q260 110 280 90" stroke="#FFE4C4" stroke-width="12" stroke-linecap="round" />
            <circle cx="280" cy="88" r="8" fill="#FFE4C4" />
            <rect x="260" y="30" width="100" height="70" rx="8" fill="rgba(255,255,255,0.9)" />
            <rect x="275" y="60" width="12" height="30" rx="2" fill="#6B5CE7" />
            <rect x="295" y="45" width="12" height="45" rx="2" fill="#8A7FE0" />
            <rect x="315" y="55" width="12" height="35" rx="2" fill="#E95CBF" />
            <path d="M340 50 L340 75 M332 58 L340 50 L348 58" stroke="#6B5CE7" stroke-width="3" stroke-linecap="round"
              stroke-linejoin="round" />
            <circle cx="150" cy="50" r="6" fill="#FFD666" />
            <circle cx="130" cy="80" r="4" fill="#FF9F43" />
            <circle cx="145" cy="120" r="5" fill="#54A0FF" />
            <path d="M150 50 Q140 65 130 80" stroke="rgba(255,255,255,0.3)" stroke-width="2" fill="none" />
            <path d="M130 80 Q135 100 145 120" stroke="rgba(255,255,255,0.3)" stroke-width="2" fill="none" />
          </svg>
        </div>
      </div>
    </div>

    <!-- 成长进度模块 -->
    <div class="progress-section">
      <div class="progress-card" v-for="item in progressItems" :key="item.title">
        <div class="progress-header">
          <span class="progress-title">{{ item.title }}</span>
          <span class="progress-value">{{ item.value }}%</span>
        </div>
        <el-progress :percentage="item.value" :stroke-width="8" :color="getProgressColor(item.title)"
          :show-text="false" />
        <div class="progress-desc">{{ item.description }}</div>
      </div>
    </div>

    <!-- AI推荐区域 -->
    <el-card class="ai-recommend-card" v-if="aiRecommendation">
      <div class="ai-header">
        <div class="ai-avatar">
          <el-icon>
            <ChatDotRound />
          </el-icon>
        </div>
        <div class="ai-info">
          <div class="ai-title">{{ aiRecommendation.title }}</div>
          <div class="ai-subtitle">{{ aiRecommendation.subtitle }}</div>
        </div>
      </div>
      <div class="ai-content">
        {{ aiRecommendation.content }}
      </div>
      <div class="ai-actions">
        <el-button type="primary" @click="$router.push('/ai')">立即咨询</el-button>
        <el-button plain @click="refreshRecommendation">换一个</el-button>
      </div>
    </el-card>

    <!-- 学习资源 -->
    <div class="section-header">
      <el-icon>
        <Reading />
      </el-icon>
      <span>学习资源</span>
    </div>
    <div class="resources-grid">
      <el-card class="resource-card" v-for="resource in learningResources" :key="resource.id">
        <div class="resource-logo" :style="{ background: resource.color }">
          {{ resource.logo }}
        </div>
        <div class="resource-content">
          <div class="resource-title">{{ resource.title }}</div>
          <div class="resource-desc">{{ resource.description }}</div>
          <div class="resource-footer">
            <el-tag size="small" :type="resource.tag_type as any">{{ resource.tag }}</el-tag>
            <el-button type="primary" link size="small" @click="viewResource(resource)">
              查看
            </el-button>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 快速操作 -->
    <div class="section-header">
      <el-icon>
        <Operation />
      </el-icon>
      <span>快速操作</span>
    </div>
    <div class="quick-actions">
      <el-button v-for="action in quickActions" :key="action.route" :type="action.button_type as any" size="large"
        @click="$router.push(action.route)">
        <el-icon>
          <component :is="getIcon(action.icon)" />
        </el-icon>
        {{ action.label }}
      </el-button>
    </div>

    <!-- 学习资源详情弹窗 -->
    <el-dialog v-model="showResourceDialog" :title="selectedResource?.title" width="800px" class="resource-dialog">
      <div class="resource-dialog-content" v-if="selectedResource">
        <div class="resource-dialog-header">
          <div class="resource-logo-large" :style="{ background: selectedResource.color }">
            {{ selectedResource.logo }}
          </div>
          <div class="resource-meta">
            <el-tag :type="selectedResource.tag_type as any">{{ selectedResource.tag }}</el-tag>
          </div>
        </div>
        <div class="article-content" v-html="renderMarkdown(selectedResource.content)"></div>
      </div>
      <template #footer>
        <el-button @click="showResourceDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ChatDotRound, Reading, Operation, Edit, User, TrendCharts, Search } from '@element-plus/icons-vue'
import { getHomeData, type HomeData, type LearningResource, type ProgressItem, type AIRecommendation, type QuickAction } from '@/api/home'

const router = useRouter()

// 状态
const loading = ref(true)
const homeData = ref<HomeData | null>(null)
const showResourceDialog = ref(false)
const selectedResource = ref<LearningResource | null>(null)

// 计算属性
const greeting = computed(() => homeData.value?.greeting || '欢迎回来')
const progressItems = computed<ProgressItem[]>(() => homeData.value?.progress_items || [])
const aiRecommendation = computed<AIRecommendation | null>(() => homeData.value?.ai_recommendation || null)
const learningResources = computed<LearningResource[]>(() => homeData.value?.learning_resources || [])
const quickActions = computed<QuickAction[]>(() => homeData.value?.quick_actions || [])

// 当前日期
const currentDate = computed(() => {
  const now = new Date()
  const weekDays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六']
  const year = now.getFullYear()
  const month = now.getMonth() + 1
  const day = now.getDate()
  const weekDay = weekDays[now.getDay()]
  return `${year}年${month}月${day}日 ${weekDay}`
})

// 获取用户ID
const getUserId = () => {
  const authStorage = localStorage.getItem('auth-storage')
  if (authStorage) {
    try {
      const authData = JSON.parse(authStorage)
      return authData?.user?.id
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
  return null
}

// 获取进度颜色
const getProgressColor = (title: string) => {
  const colors: Record<string, string> = {
    '职业测评': '#6B5CE7',
    '模拟面试': '#8A7FE0',
    '规划进度': '#E95CBF'
  }
  return colors[title] || '#6B5CE7'
}

// 获取图标组件
const getIcon = (iconName: string) => {
  const icons: Record<string, any> = {
    'Edit': Edit,
    'User': User,
    'TrendCharts': TrendCharts,
    'Search': Search
  }
  return icons[iconName] || Edit
}

// 查看资源
const viewResource = (resource: LearningResource) => {
  selectedResource.value = resource
  showResourceDialog.value = true
}

// 渲染Markdown为HTML（简单实现）
const renderMarkdown = (content: string | null) => {
  if (!content) return ''

  let html = content
    // 转义HTML特殊字符
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    // 代码块
    .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
    // 行内代码
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    // 标题
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    // 粗体和斜体
    .replace(/\*\*\*(.*?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    // 分隔线
    .replace(/^---$/gim, '<hr>')
    // 引用块
    .replace(/^&gt; (.*$)/gim, '<blockquote>$1</blockquote>')
    // 无序列表
    .replace(/^\- (.*$)/gim, '<li>$1</li>')
    // 有序列表
    .replace(/^(\d+)\. (.*$)/gim, '<li>$2</li>')
    // 换行
    .replace(/\n\n/g, '</p><p>')
    .replace(/\n/g, '<br>')
    // 清理多余的br在标签前后
    .replace(/<br><h/g, '<h')
    .replace(/<\/h(1|2|3)><br>/g, '</h$1>')
    .replace(/<br><li>/g, '<li>')
    .replace(/<\/li><br>/g, '</li>')
    .replace(/<br><hr><br>/g, '<hr>')
    .replace(/<br><pre>/g, '<pre>')
    .replace(/<\/pre><br>/g, '</pre>')
    .replace(/<br><blockquote>/g, '<blockquote>')
    .replace(/<\/blockquote><br>/g, '</blockquote>')

  // 包裹列表
  html = html.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>')
  html = html.replace(/<\/ul><br><ul>/g, '')
  html = html.replace(/<\/ul><ul>/g, '')

  // 包裹段落
  html = '<p>' + html + '</p>'
  html = html.replace(/<p><h/g, '<h')
  html = html.replace(/<\/h(1|2|3)><\/p>/g, '</h$1>')
  html = html.replace(/<p><ul>/g, '<ul>')
  html = html.replace(/<\/ul><\/p>/g, '</ul>')
  html = html.replace(/<p><pre>/g, '<pre>')
  html = html.replace(/<\/pre><\/p>/g, '</pre>')
  html = html.replace(/<p><hr><\/p>/g, '<hr>')
  html = html.replace(/<p><blockquote>/g, '<blockquote>')
  html = html.replace(/<\/blockquote><\/p>/g, '</blockquote>')

  return html
}

// 刷新推荐
const refreshRecommendation = () => {
  // 重新获取首页数据
  loadHomeData()
}

// 加载首页数据
const loadHomeData = async () => {
  const userId = getUserId()
  if (!userId) {
    loading.value = false
    return
  }

  try {
    homeData.value = await getHomeData(userId)
  } catch (error) {
    console.error('加载首页数据失败:', error)
    // 使用默认数据
    homeData.value = {
      username: '用户',
      greeting: '欢迎回来',
      progress_items: [
        { title: '职业测评', value: 0, description: '尚未完成测评' },
        { title: '模拟面试', value: 0, description: '尚未参加面试' },
        { title: '规划进度', value: 0, description: '尚未开始规划' }
      ],
      ai_recommendation: {
        title: '职业顾问',
        subtitle: '完成测评获取个性化推荐',
        content: '建议你先完成职业测评，我们将根据你的性格特点和兴趣爱好，为你提供个性化的职业建议。',
        avatar_icon: 'ChatDotRound'
      },
      learning_resources: [],
      quick_actions: [
        { label: '开始测评', icon: 'Edit', route: '/assessment', button_type: 'primary' },
        { label: '查看画像', icon: 'User', route: '/student-profile', button_type: 'success' },
        { label: '制定规划', icon: 'TrendCharts', route: '/plan', button_type: 'warning' },
        { label: '浏览岗位', icon: 'Search', route: '/jobs/list', button_type: 'default' }
      ],
      total_assessments: 0,
      total_interviews: 0,
      total_plans: 0
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadHomeData()
})
</script>

<style scoped lang="scss">
.home-page {
  padding: 0;
}

// 欢迎卡片
.welcome-card {
  background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
  border-radius: 16px;
  padding: 0;
  margin-bottom: 1.5rem;
  box-shadow: 0 8px 24px rgba(107, 92, 231, 0.3);
  overflow: hidden;

  .welcome-content {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
  }

  .welcome-left {
    color: #fff;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 2rem 2.5rem;
  }

  .welcome-date {
    font-size: 0.9rem;
    opacity: 0.85;
    margin-bottom: 0.5rem;
  }

  .welcome-text {
    font-size: 1.75rem;
    font-weight: 600;
    margin-bottom: 0.5rem;

    .username {
      color: #ffd666;
    }
  }

  .welcome-message {
    font-size: 1rem;
    opacity: 0.9;
    margin-bottom: 1.25rem;
  }

  .welcome-btn {
    width: fit-content;
    background: #fff;
    color: #6B5CE7;
    border: none;
    font-weight: 500;

    &:hover {
      background: #f5f5f5;
    }
  }

  .welcome-right {
    flex-shrink: 0;
    display: flex;
    align-items: center;
    padding-right: 1rem;

    .welcome-illustration {
      width: 320px;
      height: 200px;
    }
  }
}

// 成长进度模块
.progress-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.progress-card {
  background: #fff;
  border-radius: 12px;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .progress-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
  }

  .progress-title {
    font-weight: 600;
    color: #303133;
  }

  .progress-value {
    font-size: 1.25rem;
    font-weight: 600;
    color: #303133;
  }

  .progress-desc {
    font-size: 0.8rem;
    color: #909399;
    margin-top: 0.5rem;
  }
}

// AI推荐区域
.ai-recommend-card {
  margin-bottom: 1.5rem;
  border-radius: 12px;

  .ai-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
  }

  .ai-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6B5CE7, #8A7FE0);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 1.5rem;
  }

  .ai-title {
    font-weight: 600;
    color: #303133;
  }

  .ai-subtitle {
    font-size: 0.85rem;
    color: #909399;
  }

  .ai-content {
    color: #606266;
    line-height: 1.6;
    margin-bottom: 1rem;
  }

  .ai-actions {
    display: flex;
    gap: 0.75rem;
  }
}

// 区域标题
.section-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.125rem;
  font-weight: 600;
  color: #303133;
  margin-bottom: 1rem;

  .el-icon {
    color: #6B5CE7;
  }
}

// 学习资源
.resources-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.resource-card {
  border-radius: 12px;

  :deep(.el-card__body) {
    display: flex;
    gap: 1rem;
    padding: 1rem;
  }

  .resource-logo {
    width: 48px;
    height: 48px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 600;
    font-size: 0.875rem;
    flex-shrink: 0;
  }

  .resource-content {
    flex: 1;
    min-width: 0;
  }

  .resource-title {
    font-weight: 600;
    color: #303133;
    margin-bottom: 0.25rem;
  }

  .resource-desc {
    font-size: 0.8rem;
    color: #909399;
    line-height: 1.4;
    margin-bottom: 0.5rem;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }

  .resource-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
}

// 快速操作
.quick-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;

  .el-button {
    flex: 1;
    min-width: 140px;

    .el-icon {
      margin-right: 0.5rem;
    }
  }
}

// 学习资源详情弹窗
.resource-dialog {
  :deep(.el-dialog) {
    border-radius: 16px;
    overflow: hidden;
  }

  :deep(.el-dialog__header) {
    background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
    padding: 1.25rem 1.5rem;
    margin-right: 0;

    .el-dialog__title {
      color: #fff;
      font-size: 1.25rem;
      font-weight: 600;
    }

    .el-dialog__headerbtn {
      top: 50%;
      transform: translateY(-50%);
      right: 1.25rem;

      .el-dialog__close {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.25rem;

        &:hover {
          color: #fff;
        }
      }
    }
  }

  :deep(.el-dialog__body) {
    max-height: 65vh;
    overflow-y: auto;
    padding: 0;

    &::-webkit-scrollbar {
      width: 6px;
    }

    &::-webkit-scrollbar-track {
      background: #f5f7fa;
    }

    &::-webkit-scrollbar-thumb {
      background: #c0c4cc;
      border-radius: 3px;

      &:hover {
        background: #909399;
      }
    }
  }

  :deep(.el-dialog__footer) {
    border-top: 1px solid #ebeef5;
    padding: 1rem 1.5rem;
    background: #fafafa;
  }
}

.resource-dialog-content {
  padding: 1.5rem;

  .resource-dialog-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: linear-gradient(135deg, #f5f7fa 0%, #fff 100%);
    border-radius: 12px;
    border: 1px solid #ebeef5;
  }

  .resource-logo-large {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 600;
    font-size: 1.25rem;
    box-shadow: 0 4px 12px rgba(107, 92, 231, 0.3);
  }

  .resource-meta {
    display: flex;
    gap: 0.5rem;
  }
}

.article-content {
  line-height: 2;
  color: #303133;
  font-size: 0.95rem;

  h1 {
    font-size: 1.5rem;
    font-weight: 700;
    color: #303133;
    margin: 2rem 0 1.25rem;
    padding-bottom: 0.75rem;
    border-bottom: 3px solid #6B5CE7;
    position: relative;

    &::after {
      content: '';
      position: absolute;
      bottom: -3px;
      left: 0;
      width: 60px;
      height: 3px;
      background: #E95CBF;
    }
  }

  h2 {
    font-size: 1.2rem;
    font-weight: 600;
    color: #303133;
    margin: 1.75rem 0 1rem;
    padding: 0.5rem 0 0.5rem 1rem;
    border-left: 4px solid #6B5CE7;
    background: linear-gradient(90deg, #f5f7fa 0%, transparent 100%);
    border-radius: 0 8px 8px 0;
  }

  h3 {
    font-size: 1.05rem;
    font-weight: 600;
    color: #6B5CE7;
    margin: 1.25rem 0 0.75rem;
    padding-left: 0.5rem;
    border-left: 2px solid #8A7FE0;
  }

  p {
    margin: 0.75rem 0;
    text-align: justify;
  }

  ul,
  ol {
    margin: 0.75rem 0;
    padding-left: 1.5rem;

    li {
      margin: 0.5rem 0;
      position: relative;

      &::marker {
        color: #6B5CE7;
      }
    }
  }

  ul {
    list-style-type: none;
    padding-left: 1.25rem;

    li {
      &::before {
        content: '•';
        color: #6B5CE7;
        font-weight: bold;
        display: inline-block;
        width: 1rem;
        margin-left: -1rem;
      }
    }
  }

  strong {
    color: #6B5CE7;
    font-weight: 600;
    background: linear-gradient(transparent 60%, rgba(107, 92, 231, 0.1) 60%);
  }

  em {
    color: #E95CBF;
    font-style: normal;
  }

  code {
    background: linear-gradient(135deg, #f5f7fa 0%, #ebeef5 100%);
    padding: 0.125rem 0.5rem;
    border-radius: 4px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
    color: #E95CBF;
    border: 1px solid #e4e7ed;
  }

  pre {
    background: #282c34;
    padding: 1.25rem;
    border-radius: 12px;
    overflow-x: auto;
    margin: 1.25rem 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    code {
      background: none;
      padding: 0;
      color: #abb2bf;
      border: none;
    }
  }

  blockquote {
    margin: 1rem 0;
    padding: 1rem 1.25rem;
    border-left: 4px solid #6B5CE7;
    background: linear-gradient(90deg, #f5f7fa 0%, #fff 100%);
    border-radius: 0 8px 8px 0;
    color: #606266;
    font-style: italic;
  }

  hr {
    border: none;
    height: 2px;
    background: linear-gradient(90deg, transparent, #6B5CE7, transparent);
    margin: 2rem 0;
  }

  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
    border-radius: 8px;
    overflow: hidden;

    th,
    td {
      padding: 0.75rem 1rem;
      border: 1px solid #ebeef5;
      text-align: left;
    }

    th {
      background: #6B5CE7;
      color: #fff;
      font-weight: 600;
    }

    tr:nth-child(even) {
      background: #f5f7fa;
    }
  }
}
</style>

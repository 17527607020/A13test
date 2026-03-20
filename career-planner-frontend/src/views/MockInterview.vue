<template>
  <div class="interview-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>模拟面试</h1>
      <p class="subtitle">AI智能面试官，助你从容应对真实面试</p>
    </div>

    <!-- 面试模式选择 -->
    <div class="section-title">
      <el-icon>
        <VideoCamera />
      </el-icon>
      <span>选择面试模式</span>
    </div>
    <div class="mode-grid">
      <el-card class="mode-card" v-for="mode in interviewModes" :key="mode.id" @click="selectMode(mode)"
        :class="{ 'mode-selected': selectedMode?.id === mode.id }">
        <div class="mode-icon" :style="{ background: mode.color }">
          <el-icon>
            <component :is="mode.icon" />
          </el-icon>
        </div>
        <div class="mode-content">
          <h3>{{ mode.title }}</h3>
          <p>{{ mode.description }}</p>
          <div class="mode-tags">
            <el-tag v-for="tag in mode.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
          </div>
        </div>
        <el-button type="primary" class="start-btn" :loading="starting">
          <el-icon>
            <VideoPlay />
          </el-icon>
          开始面试
        </el-button>
      </el-card>
    </div>

    <!-- 热门岗位面试 -->
    <div class="section-title">
      <el-icon>
        <Briefcase />
      </el-icon>
      <span>热门岗位面试</span>
    </div>
    <div class="job-interview-grid" v-loading="loadingJobs">
      <div class="job-item" v-for="job in hotJobs" :key="job.id" @click="startJobInterview(job)">
        <div class="job-logo">{{ job.logo || job.name.substring(0, 2) }}</div>
        <div class="job-info">
          <div class="job-name">{{ job.name }}</div>
          <div class="job-count">{{ job.question_count || 0 }}道面试题</div>
        </div>
        <el-button type="primary" size="small" round :loading="starting">开始</el-button>
      </div>
    </div>

    <!-- 面试记录 -->
    <div class="section-title">
      <el-icon>
        <Clock />
      </el-icon>
      <span>面试记录</span>
    </div>
    <div class="records-list" v-loading="loadingRecords">
      <el-card class="record-card" v-for="record in interviewRecords" :key="record.id">
        <div class="record-header">
          <div class="record-job">{{ record.target_job || record.mode_name }}</div>
          <el-tag :type="record.total_score >= 80 ? 'success' : record.total_score >= 60 ? 'warning' : 'danger'"
            size="small">
            {{ Math.round(record.total_score) }}分
          </el-tag>
        </div>
        <div class="record-info">
          <span class="record-mode">{{ record.mode_name }}</span>
          <span class="record-date">{{ formatDate(record.completed_at || record.created_at) }}</span>
          <span class="record-count">{{ record.question_count }}道题</span>
        </div>
        <div class="record-actions">
          <el-button type="primary" link size="small" @click="viewDetail(record.id)">
            <el-icon>
              <View />
            </el-icon>
            查看详情
          </el-button>
          <el-button type="primary" link size="small" @click="retryInterview(record)">
            <el-icon>
              <RefreshRight />
            </el-icon>
            再来一次
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 空状态 -->
    <el-empty v-if="!loadingRecords && interviewRecords.length === 0" description="暂无面试记录，快去体验你的第一次模拟面试吧！" />

    <!-- 开始面试对话框 -->
    <el-dialog v-model="showStartDialog" title="开始面试" width="500px" :close-on-click-modal="false">
      <el-form :model="interviewForm" label-width="100px">
        <el-form-item label="面试模式">
          <el-tag :color="selectedMode?.color" style="color: #fff; border: none;">
            {{ selectedMode?.title }}
          </el-tag>
        </el-form-item>
        <el-form-item label="目标岗位" v-if="selectedMode?.id === 'technical'">
          <el-select v-model="interviewForm.target_job" placeholder="请选择目标岗位" style="width: 100%;">
            <el-option v-for="job in hotJobs" :key="job.code" :label="job.name" :value="job.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="题目数量">
          <el-slider v-model="interviewForm.question_count" :min="3" :max="10" :marks="questionMarks" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showStartDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmStartInterview" :loading="starting">
          开始面试
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { VideoCamera, Briefcase, Clock, VideoPlay, View, RefreshRight } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import {
  getInterviewModes,
  getJobPositions,
  getInterviewRecords,
  startInterview,
  type InterviewMode,
  type JobPosition,
  type InterviewRecordItem,
  type StartInterviewRequest
} from '@/api/interview'

const router = useRouter()

// 状态
const interviewModes = ref<InterviewMode[]>([])
const hotJobs = ref<JobPosition[]>([])
const interviewRecords = ref<InterviewRecordItem[]>([])
const selectedMode = ref<InterviewMode | null>(null)
const loadingJobs = ref(false)
const loadingRecords = ref(false)
const starting = ref(false)
const showStartDialog = ref(false)

// 表单
const interviewForm = reactive<StartInterviewRequest>({
  interview_mode: '',
  target_job: '',
  question_count: 5
})

const questionMarks = {
  3: '3题',
  5: '5题',
  7: '7题',
  10: '10题'
}

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

// 格式化日期
const formatDate = (dateStr: string | null) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载面试模式
const loadModes = async () => {
  try {
    const res = await getInterviewModes()
    interviewModes.value = res.modes || []
  } catch (error) {
    console.error('加载面试模式失败:', error)
    // 使用默认数据
    interviewModes.value = [
      {
        id: 'ai',
        title: 'AI智能面试',
        description: 'AI根据你的简历和目标岗位，智能生成面试问题',
        icon: 'Microphone',
        color: '#6B5CE7',
        tags: ['智能推荐', '个性化']
      },
      {
        id: 'behavior',
        title: '行为面试',
        description: '针对过往经历，考察你的软技能和综合素质',
        icon: 'ChatDotRound',
        color: '#E95CBF',
        tags: ['软技能', '综合素质']
      },
      {
        id: 'technical',
        title: '技术面试',
        description: '针对专业技能进行深度考察，检验技术能力',
        icon: 'Document',
        color: '#54A0FF',
        tags: ['专业技能', '深度考察']
      }
    ]
  }
}

// 加载热门岗位
const loadJobs = async () => {
  loadingJobs.value = true
  try {
    hotJobs.value = await getJobPositions(true)
  } catch (error) {
    console.error('加载岗位失败:', error)
    // 使用默认数据
    hotJobs.value = [
      { id: 1, name: 'Java开发工程师', code: 'java', logo: 'JV', question_count: 120, description: null, is_hot: true },
      { id: 2, name: '前端开发工程师', code: 'frontend', logo: 'FE', question_count: 98, description: null, is_hot: true },
      { id: 3, name: '产品经理', code: 'product', logo: 'PM', question_count: 85, description: null, is_hot: true },
      { id: 4, name: '数据分析师', code: 'data', logo: 'DA', question_count: 76, description: null, is_hot: true },
      { id: 5, name: 'Python开发工程师', code: 'python', logo: 'PY', question_count: 88, description: null, is_hot: true },
      { id: 6, name: 'UI设计师', code: 'ui', logo: 'UI', question_count: 65, description: null, is_hot: false }
    ]
  } finally {
    loadingJobs.value = false
  }
}

// 加载面试记录
const loadRecords = async () => {
  const userId = getUserId()
  if (!userId) return

  loadingRecords.value = true
  try {
    interviewRecords.value = await getInterviewRecords(userId, 10)
  } catch (error) {
    console.error('加载面试记录失败:', error)
    interviewRecords.value = []
  } finally {
    loadingRecords.value = false
  }
}

// 选择面试模式
const selectMode = (mode: InterviewMode) => {
  selectedMode.value = mode
  interviewForm.interview_mode = mode.id
  showStartDialog.value = true
}

// 开始岗位面试
const startJobInterview = (job: JobPosition) => {
  selectedMode.value = {
    id: 'technical',
    title: '技术面试',
    description: `针对${job.name}岗位的专业技能面试`,
    icon: 'Document',
    color: '#54A0FF',
    tags: [job.name]
  }
  interviewForm.interview_mode = 'technical'
  interviewForm.target_job = job.code
  showStartDialog.value = true
}

// 确认开始面试
const confirmStartInterview = async () => {
  const userId = getUserId()
  if (!userId) {
    ElMessage.error('请先登录')
    router.push('/login')
    return
  }

  starting.value = true
  try {
    const result = await startInterview(interviewForm, userId)
    showStartDialog.value = false
    ElMessage.success('面试已开始，祝你好运！')

    // 保存面试状态到 localStorage
    localStorage.setItem('interview_state', JSON.stringify({
      sessionId: result.session_id,
      questions: result.questions,
      currentIndex: 0,
      elapsedTime: 0,
      startedAt: result.started_at
    }))

    // 跳转到面试页面
    router.push({
      path: '/interview/session',
      query: {
        sessionId: result.session_id,
        total: result.total_questions
      }
    })
  } catch (error) {
    console.error('开始面试失败:', error)
    ElMessage.error('开始面试失败，请稍后重试')
  } finally {
    starting.value = false
  }
}

// 查看详情
const viewDetail = (sessionId: number) => {
  router.push(`/interview/result/${sessionId}`)
}

// 重新面试
const retryInterview = (record: InterviewRecordItem) => {
  selectedMode.value = {
    id: record.interview_mode,
    title: record.mode_name,
    description: '',
    icon: 'Document',
    color: '#6B5CE7',
    tags: []
  }
  interviewForm.interview_mode = record.interview_mode
  interviewForm.target_job = record.target_job || ''
  showStartDialog.value = true
}

onMounted(() => {
  loadModes()
  loadJobs()
  loadRecords()
})
</script>

<style scoped lang="scss">
.interview-page {
  .page-header {
    margin-bottom: 1.5rem;

    h1 {
      font-size: 1.5rem;
      font-weight: 600;
      color: #303133;
      margin-bottom: 0.25rem;
    }

    .subtitle {
      color: #909399;
      font-size: 0.9rem;
    }
  }

  .section-title {
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
}

// 面试模式网格
.mode-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;

  @media (max-width: 1200px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.mode-card {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }

  &.mode-selected {
    border-color: #6B5CE7;
  }

  :deep(.el-card__body) {
    padding: 1.5rem;
  }

  .mode-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 1rem;

    .el-icon {
      font-size: 1.75rem;
      color: #fff;
    }
  }

  .mode-content {
    h3 {
      font-size: 1.125rem;
      font-weight: 600;
      color: #303133;
      margin-bottom: 0.5rem;
    }

    p {
      color: #909399;
      font-size: 0.875rem;
      line-height: 1.5;
      margin-bottom: 0.75rem;
    }

    .mode-tags {
      display: flex;
      gap: 0.5rem;
    }
  }

  .start-btn {
    width: 100%;
    margin-top: 1rem;
    border-radius: 8px;

    .el-icon {
      margin-right: 0.5rem;
    }
  }
}

// 热门岗位面试
.job-interview-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;

  @media (max-width: 768px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.job-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #fff;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #ebeef5;

  &:hover {
    background: #f5f7fa;
    border-color: #6B5CE7;
  }

  .job-logo {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    background: linear-gradient(135deg, #6B5CE7, #8A7FE0);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-weight: 600;
    font-size: 0.8rem;
  }

  .job-info {
    flex: 1;

    .job-name {
      font-weight: 500;
      color: #303133;
      font-size: 0.9rem;
    }

    .job-count {
      font-size: 0.75rem;
      color: #909399;
    }
  }
}

// 面试记录
.records-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.record-card {
  border-radius: 12px;

  :deep(.el-card__body) {
    padding: 1.25rem;
  }

  .record-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;

    .record-job {
      font-weight: 600;
      color: #303133;
    }
  }

  .record-info {
    display: flex;
    gap: 1rem;
    font-size: 0.8rem;
    color: #909399;
    margin-bottom: 0.75rem;
  }

  .record-actions {
    display: flex;
    gap: 1rem;
  }
}
</style>

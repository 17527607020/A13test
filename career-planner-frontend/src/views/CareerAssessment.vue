<template>
  <div class="assessment-page">
    <!-- 测评选择界面 -->
    <template v-if="currentView === 'list'">
      <!-- 页面头部 -->
      <div class="page-header">
        <div class="header-left">
          <div class="header-icon">
            <el-icon :size="28">
              <Edit />
            </el-icon>
          </div>
          <div class="header-info">
            <h1 class="page-title">职业测评</h1>
            <p class="page-subtitle">科学分析自我，助力求职不迷茫</p>
          </div>
        </div>
      </div>

      <!-- 测评类型 -->
      <div class="section-title">
        <el-icon>
          <Document />
        </el-icon>
        <span>测评类型</span>
      </div>
      <div class="assessment-grid" v-loading="loading">
        <el-card class="assessment-card" v-for="item in assessments" :key="item.id" @click="startAssessment(item)">
          <div class="card-icon" :style="{ background: item.color }">
            <el-icon>
              <component :is="getIcon(item.icon)" />
            </el-icon>
          </div>
          <div class="card-content">
            <h3>{{ item.name }}</h3>
            <p>{{ item.description }}</p>
            <div class="card-meta">
              <span class="duration">
                <el-icon>
                  <Clock />
                </el-icon>
                约{{ item.duration }}分钟
              </span>
              <span class="questions">
                <el-icon>
                  <Edit />
                </el-icon>
                {{ item.question_count }}题
              </span>
            </div>
          </div>
          <el-button type="primary" class="start-btn">开始测评</el-button>
        </el-card>
      </div>

      <!-- 历史报告 -->
      <div class="section-title">
        <el-icon>
          <Folder />
        </el-icon>
        <span>历史报告</span>
      </div>
      <div class="reports-grid" v-if="reports.length > 0">
        <el-card class="report-card" v-for="report in reports" :key="report.id" @click="viewReport(report)">
          <div class="report-header">
            <div class="report-type" :style="{ background: report.color || '#6B5CE7' }">
              {{ report.assessment_type }}
            </div>
            <span class="report-date">{{ formatDate(report.completed_at) }}</span>
          </div>
          <div class="report-result">
            <div class="result-label">测评结果</div>
            <div class="result-value">{{ report.result_type }}</div>
          </div>
          <div class="report-suggestion">
            <div class="suggestion-label">结果描述</div>
            <p>{{ report.result_name }}</p>
          </div>
          <el-button type="primary" link class="view-btn">
            查看详细报告
            <el-icon>
              <ArrowRight />
            </el-icon>
          </el-button>
        </el-card>
      </div>
      <el-empty v-else description="暂无测评报告，快去完成你的第一次测评吧！" />
    </template>

    <!-- 答题界面 -->
    <template v-if="currentView === 'testing'">
      <div class="testing-container">
        <div class="testing-header">
          <el-button @click="exitTest" :icon="ArrowLeft">退出测评</el-button>
          <div class="test-info">
            <span class="test-name">{{ currentAssessment?.name }}</span>
            <span class="progress-text">第 {{ currentIndex + 1 }} / {{ questions.length }} 题</span>
          </div>
          <div class="timer">
            <el-icon>
              <Clock />
            </el-icon>
            {{ formatTime(elapsedTime) }}
          </div>
        </div>

        <el-progress :percentage="progressPercent" :stroke-width="8" :show-text="false" class="progress-bar" />

        <div class="question-container" v-if="currentQuestion">
          <div class="question-number">第 {{ currentIndex + 1 }} 题</div>
          <div class="question-text">{{ currentQuestion.question_text }}</div>

          <div class="options-list">
            <div class="option-item" v-for="option in currentQuestion.options" :key="option.value"
              :class="{ selected: answers[currentQuestion.id] === option.value }"
              @click="selectAnswer(currentQuestion.id, option.value)">
              <div class="option-indicator">{{ option.value }}</div>
              <div class="option-text">{{ option.text }}</div>
            </div>
          </div>
        </div>

        <div class="testing-footer">
          <el-button :disabled="currentIndex === 0" @click="prevQuestion">
            上一题
          </el-button>
          <el-button v-if="currentIndex < questions.length - 1" type="primary"
            :disabled="!currentQuestion || !answers[currentQuestion.id]" @click="nextQuestion">
            下一题
          </el-button>
          <el-button v-else type="primary" :disabled="!isAllAnswered" :loading="submitting" @click="submitTest">
            提交测评
          </el-button>
        </div>
      </div>
    </template>

    <!-- 测评报告界面 -->
    <template v-if="currentView === 'report'">
      <div class="report-container">
        <div class="report-header-bar">
          <el-button @click="backToList" :icon="ArrowLeft">返回列表</el-button>
          <h2>测评报告</h2>
          <el-button type="primary" @click="downloadReport">下载报告</el-button>
        </div>

        <el-card class="report-main" v-if="reportData">
          <div class="report-title-section">
            <div class="report-icon" :style="{ background: currentAssessment?.color }">
              {{ currentAssessment?.code?.toUpperCase() }}
            </div>
            <div class="report-title-info">
              <h1>{{ reportData.result_type }}</h1>
              <p>{{ reportData.result_name }}</p>
              <span class="report-date">测评时间：{{ formatDate(reportData.completed_at) }}</span>
            </div>
          </div>

          <!-- 维度分析 -->
          <div class="dimension-section" v-if="reportData.dimensions && reportData.dimensions.length > 0">
            <h3>维度分析</h3>
            <div class="dimension-list">
              <div class="dimension-item" v-for="(dim, index) in reportData.dimensions" :key="index">
                <div class="dimension-header">
                  <span class="dimension-name">{{ dim.dimension }}</span>
                  <span class="dimension-score">{{ dim.score }}/{{ dim.max_score }}</span>
                </div>
                <el-progress :percentage="dim.percentage" :stroke-width="12" :color="getDimensionColor(index)" />
              </div>
            </div>
          </div>

          <!-- 职业建议 -->
          <div class="suggestion-section" v-if="reportData.suggestions">
            <h3>职业建议</h3>
            <p>{{ reportData.suggestions }}</p>
          </div>

          <!-- 得分详情 -->
          <div class="scores-section">
            <h3>得分详情</h3>
            <div class="scores-grid">
              <div class="score-item" v-for="(value, key) in reportData.scores" :key="key">
                <span class="score-label">{{ key }}</span>
                <span class="score-value">{{ value }}</span>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Document, Clock, Edit, Folder, ArrowRight, ArrowLeft,
  User, TrendCharts, Collection
} from '@element-plus/icons-vue'
import {
  getAssessments, getAssessmentDetail, submitAssessment,
  getMyReports, getReportDetail,
  type Assessment, type AssessmentDetail, type AssessmentQuestion,
  type AssessmentReport, type ReportListItem, type AnswerSubmit
} from '@/api/assessment'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 获取当前用户ID
const userId = computed(() => userStore.user?.id || 1)

// 状态
const loading = ref(false)
const submitting = ref(false)
const currentView = ref<'list' | 'testing' | 'report'>('list')
const assessments = ref<Assessment[]>([])
const reports = ref<ReportListItem[]>([])
const currentAssessment = ref<Assessment | null>(null)
const questions = ref<AssessmentQuestion[]>([])
const currentIndex = ref(0)
const answers = ref<Record<number, string>>({})
const reportData = ref<AssessmentReport | null>(null)
const elapsedTime = ref(0)
let timer: ReturnType<typeof setInterval> | null = null

// 计算属性
const currentQuestion = computed(() => questions.value[currentIndex.value])
const progressPercent = computed(() => {
  if (questions.value.length === 0) return 0
  return ((currentIndex.value + 1) / questions.value.length) * 100
})
const isAllAnswered = computed(() => {
  return questions.value.every(q => answers.value[q.id])
})

// 方法
const getIcon = (iconName: string) => {
  const iconMap: Record<string, any> = {
    User, TrendCharts, Collection
  }
  return iconMap[iconName] || User
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

const getDimensionColor = (index: number) => {
  const colors = ['#6B5CE7', '#E95CBF', '#54A0FF', '#FF9F43', '#10B981', '#F59E0B']
  return colors[index % colors.length]
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const [assessmentsData, reportsData] = await Promise.all([
      getAssessments(),
      getMyReports(userId.value)
    ])
    assessments.value = assessmentsData
    reports.value = reportsData
  } catch (error) {
    ElMessage.error('加载数据失败')
  } finally {
    loading.value = false
  }
}

// 开始测评
const startAssessment = async (assessment: Assessment) => {
  try {
    const detail = await getAssessmentDetail(assessment.id)
    currentAssessment.value = assessment
    questions.value = detail.questions
    answers.value = {}
    currentIndex.value = 0
    elapsedTime.value = 0
    currentView.value = 'testing'

    // 开始计时
    timer = setInterval(() => {
      elapsedTime.value++
    }, 1000)
  } catch (error) {
    ElMessage.error('加载测评题目失败')
  }
}

// 选择答案
const selectAnswer = (questionId: number, value: string) => {
  answers.value[questionId] = value
}

// 上一题
const prevQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

// 下一题
const nextQuestion = () => {
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
  }
}

// 提交测评
const submitTest = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要提交测评吗？提交后无法修改答案。',
      '确认提交',
      { confirmButtonText: '确定提交', cancelButtonText: '继续答题', type: 'warning' }
    )

    submitting.value = true
    const answerList: AnswerSubmit[] = Object.entries(answers.value).map(([questionId, answer]) => ({
      question_id: Number(questionId),
      answer
    }))

    const result = await submitAssessment({
      assessment_id: currentAssessment.value!.id,
      answers: answerList
    }, userId.value)

    reportData.value = result
    currentView.value = 'report'

    // 停止计时
    if (timer) {
      clearInterval(timer)
      timer = null
    }

    ElMessage.success('测评提交成功！')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('提交测评失败')
    }
  } finally {
    submitting.value = false
  }
}

// 退出测评
const exitTest = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出测评吗？当前答题进度将不会保存。',
      '退出测评',
      { confirmButtonText: '确定退出', cancelButtonText: '继续答题', type: 'warning' }
    )

    if (timer) {
      clearInterval(timer)
      timer = null
    }
    currentView.value = 'list'
    loadData()
  } catch {
    // 取消退出
  }
}

// 查看报告
const viewReport = async (report: ReportListItem) => {
  try {
    const detail = await getReportDetail(report.id, userId.value)
    reportData.value = detail
    currentAssessment.value = detail.assessment || null
    currentView.value = 'report'
  } catch (error) {
    ElMessage.error('加载报告失败')
  }
}

// 返回列表
const backToList = () => {
  currentView.value = 'list'
  loadData()
}

// 下载报告
const downloadReport = () => {
  if (!reportData.value || !currentAssessment.value) {
    ElMessage.warning('报告数据不完整')
    return
  }

  // 生成报告HTML内容
  const reportHtml = generateReportHtml()

  // 创建Blob并下载
  const blob = new Blob([reportHtml], { type: 'text/html;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${currentAssessment.value.name}_报告_${new Date().toLocaleDateString('zh-CN').replace(/\//g, '-')}.html`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)

  ElMessage.success('报告下载成功！')
}

// 生成报告HTML
const generateReportHtml = () => {
  if (!reportData.value || !currentAssessment.value) return ''

  const report = reportData.value
  const assessment = currentAssessment.value

  return `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${assessment.name} - 测评报告</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif; 
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      min-height: 100vh;
      padding: 40px 20px;
    }
    .container {
      max-width: 800px;
      margin: 0 auto;
      background: #fff;
      border-radius: 16px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.2);
      overflow: hidden;
    }
    .header {
      background: linear-gradient(135deg, ${assessment.color || '#6B5CE7'} 0%, #8A7FE0 100%);
      color: #fff;
      padding: 40px;
      text-align: center;
    }
    .header h1 { font-size: 28px; margin-bottom: 10px; }
    .header .type { font-size: 48px; font-weight: bold; margin: 20px 0; }
    .header .desc { font-size: 18px; opacity: 0.9; }
    .content { padding: 40px; }
    .section { margin-bottom: 30px; }
    .section h2 {
      font-size: 20px;
      color: #303133;
      margin-bottom: 15px;
      padding-bottom: 10px;
      border-bottom: 2px solid ${assessment.color || '#6B5CE7'};
    }
    .dimension-item {
      margin-bottom: 15px;
    }
    .dimension-name {
      display: flex;
      justify-content: space-between;
      margin-bottom: 5px;
      font-size: 14px;
      color: #606266;
    }
    .progress-bar {
      height: 12px;
      background: #f0f0f0;
      border-radius: 6px;
      overflow: hidden;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, ${assessment.color || '#6B5CE7'} 0%, #8A7FE0 100%);
      border-radius: 6px;
    }
    .suggestion {
      background: #f5f7fa;
      padding: 20px;
      border-radius: 8px;
      font-size: 15px;
      line-height: 1.8;
      color: #606266;
    }
    .scores-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
      gap: 10px;
    }
    .score-item {
      background: #f5f7fa;
      padding: 15px 10px;
      border-radius: 8px;
      text-align: center;
    }
    .score-label { font-size: 12px; color: #909399; }
    .score-value { font-size: 20px; font-weight: bold; color: #303133; margin-top: 5px; }
    .footer {
      text-align: center;
      padding: 20px;
      color: #909399;
      font-size: 12px;
      border-top: 1px solid #e4e7ed;
    }
    @media print {
      body { background: #fff; padding: 0; }
      .container { box-shadow: none; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>${assessment.name}</h1>
      <div class="type">${report.result_type}</div>
      <div class="desc">${report.result_name}</div>
    </div>
    <div class="content">
      ${report.dimensions && report.dimensions.length > 0 ? `
      <div class="section">
        <h2>维度分析</h2>
        ${report.dimensions.map((dim, index) => `
          <div class="dimension-item">
            <div class="dimension-name">
              <span>${dim.dimension}</span>
              <span>${dim.score}/${dim.max_score}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" style="width: ${dim.percentage}%"></div>
            </div>
          </div>
        `).join('')}
      </div>
      ` : ''}
      ${report.suggestions ? `
      <div class="section">
        <h2>职业建议</h2>
        <div class="suggestion">${report.suggestions}</div>
      </div>
      ` : ''}
      <div class="section">
        <h2>得分详情</h2>
        <div class="scores-grid">
          ${Object.entries(report.scores).map(([key, value]) => `
            <div class="score-item">
              <div class="score-label">${key}</div>
              <div class="score-value">${value}</div>
            </div>
          `).join('')}
        </div>
      </div>
    </div>
    <div class="footer">
      测评时间：${formatDate(report.completed_at)} | 职业规划智能体
    </div>
  </div>
</body>
</html>
  `
}

// 生命周期
onMounted(() => {
  loadData()
})

onUnmounted(() => {
  if (timer) {
    clearInterval(timer)
  }
})
</script>

<style scoped lang="scss">
.assessment-page {

  // 页面头部
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding: 1.5rem;
    background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
    border-radius: 16px;
    box-shadow: 0 8px 24px rgba(107, 92, 231, 0.25);

    .header-left {
      display: flex;
      align-items: center;
      gap: 1rem;

      .header-icon {
        width: 56px;
        height: 56px;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
      }

      .header-info {
        .page-title {
          font-size: 1.5rem;
          font-weight: 600;
          color: #fff;
          margin: 0 0 0.25rem 0;
        }

        .page-subtitle {
          font-size: 0.9rem;
          color: rgba(255, 255, 255, 0.85);
          margin: 0;
        }
      }
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

// 测评卡片网格
.assessment-grid {
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

.assessment-card {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-card__body) {
    padding: 1.5rem;
  }

  .card-icon {
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

  .card-content {
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
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .card-meta {
      display: flex;
      gap: 1rem;
      font-size: 0.8rem;
      color: #909399;

      span {
        display: flex;
        align-items: center;
        gap: 0.25rem;

        .el-icon {
          font-size: 0.875rem;
        }
      }
    }
  }

  .start-btn {
    width: 100%;
    margin-top: 1rem;
    border-radius: 8px;
  }
}

// 报告卡片网格
.reports-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.report-card {
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  :deep(.el-card__body) {
    padding: 1.25rem;
  }

  .report-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    .report-type {
      padding: 0.25rem 0.75rem;
      border-radius: 4px;
      color: #fff;
      font-size: 0.8rem;
      font-weight: 500;
    }

    .report-date {
      font-size: 0.8rem;
      color: #909399;
    }
  }

  .report-result {
    margin-bottom: 0.75rem;

    .result-label {
      font-size: 0.8rem;
      color: #909399;
      margin-bottom: 0.25rem;
    }

    .result-value {
      font-size: 1.25rem;
      font-weight: 600;
      color: #303133;
    }
  }

  .report-suggestion {
    margin-bottom: 0.75rem;

    .suggestion-label {
      font-size: 0.8rem;
      color: #909399;
      margin-bottom: 0.25rem;
    }

    p {
      font-size: 0.875rem;
      color: #606266;
      line-height: 1.5;
    }
  }

  .view-btn {
    padding: 0;
    font-size: 0.875rem;

    .el-icon {
      margin-left: 0.25rem;
    }
  }
}

// 答题界面
.testing-container {
  .testing-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    .test-info {
      text-align: center;

      .test-name {
        font-weight: 600;
        color: #303133;
        margin-right: 1rem;
      }

      .progress-text {
        color: #909399;
        font-size: 0.875rem;
      }
    }

    .timer {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 1.125rem;
      font-weight: 500;
      color: #606266;
    }
  }

  .progress-bar {
    margin-bottom: 2rem;
  }

  .question-container {
    background: #fff;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

    .question-number {
      font-size: 0.875rem;
      color: #909399;
      margin-bottom: 0.75rem;
    }

    .question-text {
      font-size: 1.25rem;
      font-weight: 500;
      color: #303133;
      line-height: 1.6;
      margin-bottom: 2rem;
    }

    .options-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }

    .option-item {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem 1.25rem;
      border: 2px solid #e4e7ed;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.2s;

      &:hover {
        border-color: #6B5CE7;
        background: #f5f3ff;
      }

      &.selected {
        border-color: #6B5CE7;
        background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);

        .option-indicator {
          background: #fff;
          color: #6B5CE7;
        }

        .option-text {
          color: #fff;
        }
      }

      .option-indicator {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #f5f7fa;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        color: #606266;
        flex-shrink: 0;
      }

      .option-text {
        font-size: 1rem;
        color: #303133;
      }
    }
  }

  .testing-footer {
    display: flex;
    justify-content: center;
    gap: 1rem;
  }
}

// 报告界面
.report-container {
  .report-header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;

    h2 {
      font-size: 1.25rem;
      font-weight: 600;
      color: #303133;
    }
  }

  .report-main {
    border-radius: 16px;

    :deep(.el-card__body) {
      padding: 2rem;
    }
  }

  .report-title-section {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #e4e7ed;

    .report-icon {
      width: 80px;
      height: 80px;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      font-weight: 700;
      color: #fff;
    }

    .report-title-info {
      h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #303133;
        margin-bottom: 0.5rem;
      }

      p {
        font-size: 1.125rem;
        color: #606266;
        margin-bottom: 0.25rem;
      }

      .report-date {
        font-size: 0.875rem;
        color: #909399;
      }
    }
  }

  .dimension-section,
  .suggestion-section,
  .scores-section {
    margin-bottom: 2rem;

    h3 {
      font-size: 1.125rem;
      font-weight: 600;
      color: #303133;
      margin-bottom: 1rem;
    }
  }

  .dimension-list {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .dimension-item {
    .dimension-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;

      .dimension-name {
        font-size: 0.875rem;
        color: #606266;
      }

      .dimension-score {
        font-size: 0.875rem;
        font-weight: 500;
        color: #303133;
      }
    }
  }

  .suggestion-section {
    p {
      font-size: 1rem;
      color: #606266;
      line-height: 1.8;
      background: #f5f7fa;
      padding: 1rem 1.25rem;
      border-radius: 8px;
    }
  }

  .scores-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
    gap: 0.75rem;

    .score-item {
      background: #f5f7fa;
      padding: 0.75rem;
      border-radius: 8px;
      text-align: center;

      .score-label {
        display: block;
        font-size: 0.75rem;
        color: #909399;
        margin-bottom: 0.25rem;
      }

      .score-value {
        font-size: 1.25rem;
        font-weight: 600;
        color: #303133;
      }
    }
  }
}
</style>

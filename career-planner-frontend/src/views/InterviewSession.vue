<template>
  <div class="interview-session-page">
    <!-- 顶部状态栏 -->
    <div class="status-bar">
      <div class="status-left">
        <el-button @click="exitInterview" :disabled="submitting">
          <el-icon>
            <ArrowLeft />
          </el-icon>
          退出面试
        </el-button>
      </div>
      <div class="status-center">
        <div class="progress-info">
          <span class="current">第 {{ currentIndex + 1 }} 题</span>
          <span class="divider">/</span>
          <span class="total">共 {{ totalQuestions }} 题</span>
        </div>
        <el-progress :percentage="progressPercent" :stroke-width="8" :show-text="false" class="progress-bar" />
      </div>
      <div class="status-right">
        <div class="timer" :class="{ 'timer-warning': elapsedTime > 30 * 60 }">
          <el-icon>
            <Timer />
          </el-icon>
          <span>{{ formatTime(elapsedTime) }}</span>
        </div>
      </div>
    </div>

    <!-- 面试内容区 -->
    <div class="interview-content" v-if="currentQuestion">
      <!-- 题目卡片 -->
      <el-card class="question-card">
        <div class="question-header">
          <div class="question-meta">
            <el-tag :type="getDifficultyType(currentQuestion.difficulty)" size="small">
              {{ getDifficultyLabel(currentQuestion.difficulty) }}
            </el-tag>
            <el-tag v-if="currentQuestion.category" type="info" size="small">
              {{ getCategoryLabel(currentQuestion.category) }}
            </el-tag>
          </div>
          <div class="question-number">Q{{ currentIndex + 1 }}</div>
        </div>
        <div class="question-text">
          {{ currentQuestion.question_text }}
        </div>
        <div class="question-tags" v-if="currentQuestion.tags?.length">
          <el-tag v-for="tag in currentQuestion.tags" :key="tag" size="small" type="info" effect="plain">
            {{ tag }}
          </el-tag>
        </div>
      </el-card>

      <!-- 回答区域 -->
      <el-card class="answer-card">
        <template #header>
          <div class="answer-header">
            <span>你的回答</span>
            <span class="char-count">{{ answerText.length }} 字</span>
          </div>
        </template>
        <el-input v-model="answerText" type="textarea" :rows="8" :placeholder="answerPlaceholder" :disabled="submitting"
          @input="onAnswerChange" />
        <div class="answer-actions">
          <div class="answer-timer">
            <el-icon>
              <Clock />
            </el-icon>
            <span>本题用时: {{ formatTime(questionTime) }}</span>
          </div>
          <div class="action-buttons">
            <el-button @click="skipQuestion" :disabled="submitting">
              跳过此题
            </el-button>
            <el-button type="primary" @click="submitAnswer" :loading="submitting" :disabled="!answerText.trim()">
              提交回答
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- 答题反馈（提交后显示） -->
      <el-card v-if="currentFeedback" class="feedback-card">
        <template #header>
          <div class="feedback-header">
            <span>AI评分反馈</span>
            <el-tag :type="getScoreType(currentFeedback.score)" size="large">
              {{ Math.round(currentFeedback.score) }} 分
            </el-tag>
          </div>
        </template>

        <!-- 评分详情 -->
        <div class="score-details" v-if="currentFeedback.score_details">
          <div class="score-item">
            <span class="score-label">相关性</span>
            <el-progress :percentage="currentFeedback.score_details.relevance" :stroke-width="10"
              :color="getScoreColor(currentFeedback.score_details.relevance)" />
          </div>
          <div class="score-item">
            <span class="score-label">深度</span>
            <el-progress :percentage="currentFeedback.score_details.depth" :stroke-width="10"
              :color="getScoreColor(currentFeedback.score_details.depth)" />
          </div>
          <div class="score-item">
            <span class="score-label">清晰度</span>
            <el-progress :percentage="currentFeedback.score_details.clarity" :stroke-width="10"
              :color="getScoreColor(currentFeedback.score_details.clarity)" />
          </div>
          <div class="score-item">
            <span class="score-label">完整性</span>
            <el-progress :percentage="currentFeedback.score_details.completeness" :stroke-width="10"
              :color="getScoreColor(currentFeedback.score_details.completeness)" />
          </div>
        </div>

        <!-- 反馈内容 -->
        <div class="feedback-content">
          <div class="feedback-item">
            <div class="feedback-title">
              <el-icon>
                <ChatDotRound />
              </el-icon>
              总体评价
            </div>
            <p>{{ currentFeedback.feedback }}</p>
          </div>
          <div class="feedback-item" v-if="currentFeedback.suggestions">
            <div class="feedback-title">
              <el-icon>
                <TrendCharts />
              </el-icon>
              改进建议
            </div>
            <p>{{ currentFeedback.suggestions }}</p>
          </div>
          <div class="feedback-item" v-if="currentFeedback.reference_answer">
            <div class="feedback-title">
              <el-icon>
                <Document />
              </el-icon>
              参考答案
            </div>
            <p class="reference-answer">{{ currentFeedback.reference_answer }}</p>
          </div>
        </div>

        <div class="feedback-actions">
          <el-button type="primary" @click="nextQuestion">
            {{ isLastQuestion ? '完成面试' : '下一题' }}
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 退出确认对话框 -->
    <el-dialog v-model="showExitDialog" title="确认退出" width="400px">
      <p>确定要退出面试吗？当前进度将不会保存。</p>
      <template #footer>
        <el-button @click="showExitDialog = false">继续面试</el-button>
        <el-button type="danger" @click="confirmExit">确认退出</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Timer, Clock, ChatDotRound, TrendCharts, Document } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  submitAnswer as submitAnswerApi,
  completeInterview as completeInterviewApi,
  type InterviewQuestion,
  type AnswerFeedback
} from '@/api/interview'

const route = useRoute()
const router = useRouter()

// 状态
const sessionId = ref<number>(0)
const totalQuestions = ref(0)
const questions = ref<InterviewQuestion[]>([])
const currentIndex = ref(0)
const answerText = ref('')
const submitting = ref(false)
const currentFeedback = ref<AnswerFeedback | null>(null)
const showExitDialog = ref(false)

// 回答提示
const answerPlaceholder = `请在此输入你的回答...

提示：
• 条理清晰地组织你的回答
• 可以使用"首先、其次、最后"等结构化表达
• 结合具体案例和经验来支撑你的观点
• 回答越详细，评分越准确`

// 计时器
const elapsedTime = ref(0)
const questionTime = ref(0)
let timer: number | null = null
let questionTimer: number | null = null

// 当前题目
const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || null
})

// 进度百分比
const progressPercent = computed(() => {
  if (totalQuestions.value === 0) return 0
  return Math.round(((currentIndex.value) / totalQuestions.value) * 100)
})

// 是否最后一题
const isLastQuestion = computed(() => {
  return currentIndex.value >= totalQuestions.value - 1
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

// 格式化时间
const formatTime = (seconds: number) => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 获取难度类型
const getDifficultyType = (difficulty: string) => {
  const map: Record<string, string> = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return map[difficulty] || 'info'
}

// 获取难度标签
const getDifficultyLabel = (difficulty: string) => {
  const map: Record<string, string> = {
    easy: '简单',
    medium: '中等',
    hard: '困难'
  }
  return map[difficulty] || difficulty
}

// 获取分类标签
const getCategoryLabel = (category: string) => {
  const map: Record<string, string> = {
    technical: '技术',
    behavioral: '行为',
    general: '综合',
    ai: 'AI智能'
  }
  return map[category] || category
}

// 获取分数类型
const getScoreType = (score: number) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

// 获取分数颜色
const getScoreColor = (score: number) => {
  if (score >= 80) return '#67C23A'
  if (score >= 60) return '#E6A23C'
  return '#F56C6C'
}

// 开始计时
const startTimer = () => {
  timer = window.setInterval(() => {
    elapsedTime.value++
  }, 1000)

  questionTimer = window.setInterval(() => {
    questionTime.value++
  }, 1000)
}

// 停止计时
const stopTimer = () => {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  if (questionTimer) {
    clearInterval(questionTimer)
    questionTimer = null
  }
}

// 回答变化
const onAnswerChange = () => {
  // 可以在这里添加自动保存逻辑
}

// 提交回答
const submitAnswer = async () => {
  if (!answerText.value.trim()) {
    ElMessage.warning('请输入你的回答')
    return
  }

  const userId = getUserId()
  if (!userId || !currentQuestion.value) return

  submitting.value = true
  try {
    const feedback = await submitAnswerApi({
      session_id: sessionId.value,
      question_id: currentQuestion.value.id,
      user_answer: answerText.value,
      answer_duration: questionTime.value
    }, userId)

    currentFeedback.value = feedback
    ElMessage.success('回答已提交')
  } catch (error) {
    console.error('提交回答失败:', error)
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 跳过题目
const skipQuestion = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要跳过这道题吗？跳过后将不得分。',
      '提示',
      {
        confirmButtonText: '确定跳过',
        cancelButtonText: '继续作答',
        type: 'warning'
      }
    )

    // 提交空回答
    const userId = getUserId()
    if (userId && currentQuestion.value) {
      await submitAnswerApi({
        session_id: sessionId.value,
        question_id: currentQuestion.value.id,
        user_answer: '（跳过未作答）',
        answer_duration: questionTime.value
      }, userId)
    }

    nextQuestion()
  } catch {
    // 用户取消
  }
}

// 下一题
const nextQuestion = async () => {
  if (isLastQuestion.value) {
    // 完成面试
    await finishInterview()
  } else {
    // 下一题
    currentIndex.value++
    answerText.value = ''
    currentFeedback.value = null
    questionTime.value = 0
  }
}

// 完成面试
const finishInterview = async () => {
  const userId = getUserId()
  if (!userId) return

  submitting.value = true
  try {
    await completeInterviewApi(sessionId.value, userId)
    ElMessage.success('面试已完成！')

    // 跳转到结果页面
    router.push(`/interview/result/${sessionId.value}`)
  } catch (error) {
    console.error('完成面试失败:', error)
    ElMessage.error('操作失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 退出面试
const exitInterview = () => {
  showExitDialog.value = true
}

// 确认退出
const confirmExit = () => {
  stopTimer()
  router.push('/interview')
}

// 初始化
onMounted(() => {
  // 从路由参数获取面试信息
  sessionId.value = Number(route.query.sessionId) || 0
  totalQuestions.value = Number(route.query.total) || 0

  // 从 localStorage 恢复面试状态
  const interviewState = localStorage.getItem('interview_state')
  if (interviewState) {
    try {
      const state = JSON.parse(interviewState)
      if (state.sessionId === sessionId.value) {
        questions.value = state.questions || []
        currentIndex.value = state.currentIndex || 0
        elapsedTime.value = state.elapsedTime || 0
      }
    } catch (e) {
      console.error('恢复面试状态失败:', e)
    }
  }

  // 如果没有题目数据，返回首页
  if (questions.value.length === 0 && totalQuestions.value === 0) {
    ElMessage.error('面试数据异常，请重新开始')
    router.push('/interview')
    return
  }

  // 开始计时
  startTimer()
})

// 保存状态
const saveState = () => {
  localStorage.setItem('interview_state', JSON.stringify({
    sessionId: sessionId.value,
    questions: questions.value,
    currentIndex: currentIndex.value,
    elapsedTime: elapsedTime.value
  }))
}

// 页面离开前保存状态
onUnmounted(() => {
  stopTimer()
  saveState()
})
</script>

<style scoped lang="scss">
.interview-session-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 2rem;
}

// 状态栏
.status-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 2rem;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);

  .status-center {
    flex: 1;
    max-width: 400px;
    margin: 0 2rem;

    .progress-info {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 0.5rem;
      margin-bottom: 0.5rem;
      font-size: 0.9rem;

      .current {
        font-weight: 600;
        color: #6B5CE7;
      }

      .divider {
        color: #dcdfe6;
      }

      .total {
        color: #909399;
      }
    }

    .progress-bar {
      width: 100%;
    }
  }

  .timer {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    background: #f5f7fa;
    border-radius: 20px;
    font-size: 1rem;
    font-weight: 500;
    color: #606266;

    &.timer-warning {
      background: #fef0f0;
      color: #f56c6c;
    }
  }
}

// 面试内容
.interview-content {
  max-width: 900px;
  margin: 2rem auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

// 题目卡片
.question-card {
  border-radius: 12px;

  .question-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    .question-meta {
      display: flex;
      gap: 0.5rem;
    }

    .question-number {
      font-size: 1.5rem;
      font-weight: 700;
      color: #6B5CE7;
      opacity: 0.3;
    }
  }

  .question-text {
    font-size: 1.25rem;
    line-height: 1.8;
    color: #303133;
    margin-bottom: 1rem;
  }

  .question-tags {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
  }
}

// 回答卡片
.answer-card {
  border-radius: 12px;

  .answer-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .char-count {
      color: #909399;
      font-size: 0.875rem;
    }
  }

  :deep(.el-textarea__inner) {
    font-size: 1rem;
    line-height: 1.8;
  }

  .answer-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #ebeef5;

    .answer-timer {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: #909399;
      font-size: 0.875rem;
    }

    .action-buttons {
      display: flex;
      gap: 1rem;
    }
  }
}

// 反馈卡片
.feedback-card {
  border-radius: 12px;
  border: 2px solid #6B5CE7;

  .feedback-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .score-details {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: #f5f7fa;
    border-radius: 8px;

    .score-item {
      .score-label {
        display: block;
        font-size: 0.875rem;
        color: #606266;
        margin-bottom: 0.5rem;
      }
    }
  }

  .feedback-content {
    .feedback-item {
      margin-bottom: 1.5rem;

      &:last-child {
        margin-bottom: 0;
      }

      .feedback-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        color: #303133;
        margin-bottom: 0.5rem;

        .el-icon {
          color: #6B5CE7;
        }
      }

      p {
        color: #606266;
        line-height: 1.8;
        margin: 0;
      }

      .reference-answer {
        padding: 1rem;
        background: #f5f7fa;
        border-radius: 8px;
        border-left: 3px solid #6B5CE7;
      }
    }
  }

  .feedback-actions {
    display: flex;
    justify-content: center;
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid #ebeef5;
  }
}

@media (max-width: 768px) {
  .status-bar {
    flex-wrap: wrap;
    gap: 1rem;
    padding: 1rem;

    .status-center {
      order: 3;
      width: 100%;
      max-width: none;
      margin: 0;
    }
  }

  .interview-content {
    margin: 1rem auto;
  }

  .score-details {
    grid-template-columns: 1fr !important;
  }
}
</style>

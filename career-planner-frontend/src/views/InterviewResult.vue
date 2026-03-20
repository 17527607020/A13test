<template>
  <div class="interview-result-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading" :size="48">
        <Loading />
      </el-icon>
      <p>正在加载面试结果...</p>
    </div>

    <!-- 结果内容 -->
    <div v-else-if="sessionDetail" class="result-content">
      <!-- 头部概览 -->
      <div class="result-header">
        <div class="header-left">
          <el-button @click="goBack">
            <el-icon>
              <ArrowLeft />
            </el-icon>
            返回
          </el-button>
        </div>
        <div class="header-title">
          <h1>面试报告</h1>
          <p>{{ sessionDetail.target_job || '综合面试' }}</p>
        </div>
        <div class="header-right">
          <el-button type="primary" @click="retryInterview">
            <el-icon>
              <RefreshRight />
            </el-icon>
            再来一次
          </el-button>
        </div>
      </div>

      <!-- 总分卡片 -->
      <el-card class="score-card">
        <div class="score-main">
          <div class="score-circle" :style="{ background: getScoreColor(sessionDetail.total_score) }">
            <span class="score-number">{{ Math.round(sessionDetail.total_score) }}</span>
            <span class="score-unit">分</span>
          </div>
          <div class="score-info">
            <div class="score-level">{{ getScoreLevel(sessionDetail.total_score) }}</div>
            <div class="score-desc">{{ getScoreDesc(sessionDetail.total_score) }}</div>
            <div class="score-meta">
              <span>
                <el-icon>
                  <Timer />
                </el-icon>
                用时 {{ sessionDetail.duration }} 分钟
              </span>
              <span>
                <el-icon>
                  <Document />
                </el-icon>
                {{ sessionDetail.answers?.length || 0 }} 道题
              </span>
            </div>
          </div>
        </div>

        <!-- 优劣势分析 -->
        <div class="analysis-section" v-if="sessionDetail.strengths?.length || sessionDetail.improvements?.length">
          <div class="analysis-item" v-if="sessionDetail.strengths?.length">
            <div class="analysis-title success">
              <el-icon>
                <CircleCheck />
              </el-icon>
              优势
            </div>
            <div class="analysis-tags">
              <el-tag v-for="item in sessionDetail.strengths" :key="item" type="success" effect="plain">
                {{ item }}
              </el-tag>
            </div>
          </div>
          <div class="analysis-item" v-if="sessionDetail.improvements?.length">
            <div class="analysis-title warning">
              <el-icon>
                <Warning />
              </el-icon>
              待改进
            </div>
            <div class="analysis-tags">
              <el-tag v-for="item in sessionDetail.improvements" :key="item" type="warning" effect="plain">
                {{ item }}
              </el-tag>
            </div>
          </div>
        </div>

        <!-- 总体反馈 -->
        <div class="overall-feedback" v-if="sessionDetail.overall_feedback">
          <div class="feedback-title">
            <el-icon>
              <ChatDotRound />
            </el-icon>
            总体评价
          </div>
          <p>{{ sessionDetail.overall_feedback }}</p>
        </div>
      </el-card>

      <!-- 答题详情 -->
      <div class="answers-section">
        <div class="section-title">
          <el-icon>
            <List />
          </el-icon>
          答题详情
        </div>

        <el-collapse v-model="activeAnswers" accordion>
          <el-collapse-item v-for="(answer, index) in sessionDetail.answers" :key="answer.id" :name="index">
            <template #title>
              <div class="answer-title">
                <span class="question-index">Q{{ index + 1 }}</span>
                <span class="question-preview">{{ answer.question_text }}</span>
                <el-tag :type="getScoreType(answer.score)" size="small" class="answer-score">
                  {{ Math.round(answer.score) }}分
                </el-tag>
              </div>
            </template>

            <div class="answer-detail">
              <!-- 评分详情 -->
              <div class="detail-section" v-if="answer.score_details">
                <div class="detail-title">评分维度</div>
                <div class="score-dimensions">
                  <div class="dimension-item">
                    <span class="dimension-label">相关性</span>
                    <el-progress :percentage="answer.score_details.relevance"
                      :color="getScoreColor(answer.score_details.relevance)" :stroke-width="8" />
                  </div>
                  <div class="dimension-item">
                    <span class="dimension-label">深度</span>
                    <el-progress :percentage="answer.score_details.depth"
                      :color="getScoreColor(answer.score_details.depth)" :stroke-width="8" />
                  </div>
                  <div class="dimension-item">
                    <span class="dimension-label">清晰度</span>
                    <el-progress :percentage="answer.score_details.clarity"
                      :color="getScoreColor(answer.score_details.clarity)" :stroke-width="8" />
                  </div>
                  <div class="dimension-item">
                    <span class="dimension-label">完整性</span>
                    <el-progress :percentage="answer.score_details.completeness"
                      :color="getScoreColor(answer.score_details.completeness)" :stroke-width="8" />
                  </div>
                </div>
              </div>

              <!-- 我的回答 -->
              <div class="detail-section">
                <div class="detail-title">我的回答</div>
                <div class="answer-content">{{ answer.user_answer || '（未作答）' }}</div>
              </div>

              <!-- AI反馈 -->
              <div class="detail-section" v-if="answer.feedback">
                <div class="detail-title">AI反馈</div>
                <div class="feedback-content">{{ answer.feedback }}</div>
              </div>

              <!-- 改进建议 -->
              <div class="detail-section" v-if="answer.suggestions">
                <div class="detail-title">改进建议</div>
                <div class="suggestion-content">{{ answer.suggestions }}</div>
              </div>

              <!-- 参考答案 -->
              <div class="detail-section" v-if="answer.reference_answer">
                <div class="detail-title">参考答案</div>
                <div class="reference-content">{{ answer.reference_answer }}</div>
              </div>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 操作按钮 -->
      <div class="action-buttons">
        <el-button size="large" @click="goBack">返回列表</el-button>
        <el-button type="primary" size="large" @click="retryInterview">
          再来一次
        </el-button>
      </div>
    </div>

    <!-- 错误状态 -->
    <el-empty v-else description="面试记录不存在或已过期">
      <el-button type="primary" @click="goBack">返回面试列表</el-button>
    </el-empty>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  ArrowLeft,
  RefreshRight,
  Timer,
  Document,
  CircleCheck,
  Warning,
  ChatDotRound,
  List,
  Loading
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getSessionDetail, type InterviewSessionDetail } from '@/api/interview'

const route = useRoute()
const router = useRouter()

// 状态
const loading = ref(true)
const sessionDetail = ref<InterviewSessionDetail | null>(null)
const activeAnswers = ref<number[]>([])

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

// 获取分数颜色
const getScoreColor = (score: number) => {
  if (score >= 80) return '#67C23A'
  if (score >= 60) return '#E6A23C'
  return '#F56C6C'
}

// 获取分数类型
const getScoreType = (score: number) => {
  if (score >= 80) return 'success'
  if (score >= 60) return 'warning'
  return 'danger'
}

// 获取分数等级
const getScoreLevel = (score: number) => {
  if (score >= 90) return '优秀'
  if (score >= 80) return '良好'
  if (score >= 70) return '中等'
  if (score >= 60) return '及格'
  return '需加强'
}

// 获取分数描述
const getScoreDesc = (score: number) => {
  if (score >= 90) return '表现非常出色，继续保持！'
  if (score >= 80) return '表现良好，还有提升空间'
  if (score >= 70) return '表现中等，建议加强练习'
  if (score >= 60) return '刚刚及格，需要更多努力'
  return '表现欠佳，建议重新准备'
}

// 返回
const goBack = () => {
  router.push('/interview')
}

// 重新面试
const retryInterview = () => {
  router.push('/interview')
}

// 加载详情
const loadDetail = async () => {
  const sessionId = Number(route.params.id)
  const userId = getUserId()

  if (!sessionId || !userId) {
    loading.value = false
    return
  }

  try {
    sessionDetail.value = await getSessionDetail(sessionId, userId)
  } catch (error) {
    console.error('加载面试详情失败:', error)
    ElMessage.error('加载失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped lang="scss">
.interview-result-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 2rem;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 400px;
  color: #909399;

  .el-icon {
    margin-bottom: 1rem;
  }
}

.result-content {
  max-width: 900px;
  margin: 0 auto;
}

// 头部
.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;

  .header-title {
    text-align: center;

    h1 {
      font-size: 1.5rem;
      font-weight: 600;
      color: #303133;
      margin: 0;
    }

    p {
      color: #909399;
      margin: 0.25rem 0 0;
    }
  }
}

// 总分卡片
.score-card {
  border-radius: 16px;
  margin-bottom: 2rem;

  :deep(.el-card__body) {
    padding: 2rem;
  }

  .score-main {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 2rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid #ebeef5;

    @media (max-width: 768px) {
      flex-direction: column;
      text-align: center;
    }
  }

  .score-circle {
    width: 140px;
    height: 140px;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #fff;
    flex-shrink: 0;

    .score-number {
      font-size: 3rem;
      font-weight: 700;
      line-height: 1;
    }

    .score-unit {
      font-size: 1rem;
      opacity: 0.8;
    }
  }

  .score-info {
    flex: 1;

    .score-level {
      font-size: 1.5rem;
      font-weight: 600;
      color: #303133;
      margin-bottom: 0.5rem;
    }

    .score-desc {
      color: #606266;
      margin-bottom: 1rem;
    }

    .score-meta {
      display: flex;
      gap: 1.5rem;
      color: #909399;
      font-size: 0.875rem;

      span {
        display: flex;
        align-items: center;
        gap: 0.25rem;
      }
    }
  }

  .analysis-section {
    display: flex;
    gap: 2rem;
    margin-bottom: 1.5rem;

    @media (max-width: 768px) {
      flex-direction: column;
      gap: 1rem;
    }

    .analysis-item {
      flex: 1;

      .analysis-title {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-weight: 600;
        margin-bottom: 0.75rem;

        &.success {
          color: #67C23A;
        }

        &.warning {
          color: #E6A23C;
        }
      }

      .analysis-tags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
      }
    }
  }

  .overall-feedback {
    background: #f5f7fa;
    padding: 1rem;
    border-radius: 8px;

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
  }
}

// 答题详情
.answers-section {
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

  .answer-title {
    display: flex;
    align-items: center;
    gap: 1rem;
    width: 100%;

    .question-index {
      font-weight: 600;
      color: #6B5CE7;
      min-width: 30px;
    }

    .question-preview {
      flex: 1;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .answer-score {
      flex-shrink: 0;
    }
  }

  .answer-detail {
    padding: 1rem 0;

    .detail-section {
      margin-bottom: 1.5rem;

      &:last-child {
        margin-bottom: 0;
      }

      .detail-title {
        font-weight: 600;
        color: #303133;
        margin-bottom: 0.5rem;
        padding-left: 0.5rem;
        border-left: 3px solid #6B5CE7;
      }

      .score-dimensions {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 1rem;

        @media (max-width: 768px) {
          grid-template-columns: 1fr;
        }

        .dimension-item {
          .dimension-label {
            display: block;
            font-size: 0.875rem;
            color: #606266;
            margin-bottom: 0.25rem;
          }
        }
      }

      .answer-content,
      .feedback-content,
      .suggestion-content,
      .reference-content {
        padding: 1rem;
        background: #f5f7fa;
        border-radius: 8px;
        color: #606266;
        line-height: 1.8;
      }

      .reference-content {
        background: #fdf6ec;
        border-left: 3px solid #E6A23C;
      }
    }
  }
}

// 操作按钮
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}
</style>

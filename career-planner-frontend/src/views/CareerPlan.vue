<template>
  <div class="career-plan-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <el-icon :size="28">
            <TrendCharts />
          </el-icon>
        </div>
        <div class="header-info">
          <h1 class="page-title">职业规划</h1>
          <p class="page-subtitle">制定个性化职业发展路径，实现职业目标</p>
        </div>
      </div>
      <div class="profile-info" v-if="studentProfile">
        当前画像：{{ studentProfile.name }} - {{ studentProfile.major }} ({{ studentProfile.education }})
      </div>
    </div>

    <!-- 选择目标岗位 -->
    <el-card v-if="!matchResult">
      <template #header>
        <div>
          <span class="card-title">选择目标岗位</span>
          <p class="card-desc">基于您的学生画像，系统将为您分析匹配度并制定职业发展路径</p>
        </div>
      </template>

      <div class="job-select-area">
        <div class="search-box">
          <label class="search-label">搜索岗位</label>
          <el-input v-model="searchKeyword" placeholder="输入岗位名称..." />
        </div>

        <div class="jobs-grid" v-if="jobs.length > 0">
          <div v-for="job in jobs" :key="job.id" class="job-option" :class="{ selected: selectedJob?.id === job.id }"
            @click="selectedJob = job">
            <h4 class="job-name">{{ job.name }}</h4>
            <div class="job-info">
              <p><span class="label">行业：</span>{{ job.industry }}</p>
              <p><span class="label">类型：</span>{{ job.type }}</p>
              <p><span class="label">薪资：</span>{{ job.salary_min }}-{{ job.salary_max }}K</p>
            </div>
          </div>
        </div>

        <el-empty v-else description="暂无岗位数据，请先在岗位探索页面创建岗位数据" />

        <el-button type="primary" size="large" class="match-btn" :disabled="!selectedJob">
          开始人岗匹配
        </el-button>
      </div>
    </el-card>

    <!-- 匹配结果 -->
    <div v-else class="match-result">
      <!-- 学生画像摘要 -->
      <el-card class="profile-summary">
        <h3 class="summary-title">
          <el-icon>
            <User />
          </el-icon>
          您的学生画像
        </h3>
        <div class="summary-grid">
          <div><span class="label">姓名：</span><span class="value">张三</span></div>
          <div><span class="label">学校：</span><span class="value">清华大学</span></div>
          <div><span class="label">专业：</span><span class="value">计算机科学</span></div>
          <div><span class="label">学历：</span><span class="value">本科</span></div>
        </div>
      </el-card>

      <!-- 匹配结果 -->
      <el-card>
        <template #header>
          <span class="card-title">匹配结果：{{ selectedJob?.name }}</span>
        </template>
        <div class="result-content">
          <div class="score-section">
            <h4>整体匹配度</h4>
            <div class="score-value">85%</div>
            <p class="score-desc">匹配度很高，建议立即申请</p>
          </div>
          <div class="radar-section">
            <h4>维度对比</h4>
            <div class="radar-placeholder">雷达图区域</div>
          </div>
        </div>
      </el-card>

      <!-- 职业发展路径 -->
      <el-card>
        <template #header>
          <div>
            <span class="card-title">职业发展路径</span>
            <p class="card-desc">基于计算机科学专业背景与Java开发工程师岗位要求制定</p>
          </div>
        </template>
        <div class="career-path">
          <div v-for="(item, index) in careerPath" :key="index" class="path-item">
            <div class="path-number">{{ index + 1 }}</div>
            <h4 class="path-stage">{{ item.stage }}</h4>
            <ul class="path-actions">
              <li v-for="(action, i) in item.actions" :key="i">{{ action }}</li>
            </ul>
          </div>
        </div>
      </el-card>

      <div class="action-buttons">
        <el-button type="primary">生成完整报告</el-button>
        <el-button @click="resetMatch">重新选择岗位</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { User, TrendCharts } from '@element-plus/icons-vue'

const searchKeyword = ref('')
const selectedJob = ref<any>(null)
const matchResult = ref<any>(null)
const studentProfile = ref({
  name: '张三',
  major: '计算机科学',
  education: '本科'
})

const jobs = ref([
  { id: '1', name: 'Java开发工程师', type: '开发', industry: '互联网', salary_min: 10, salary_max: 15 },
  { id: '2', name: '产品经理', type: '产品', industry: '互联网', salary_min: 8, salary_max: 12 },
  { id: '3', name: '前端开发工程师', type: '开发', industry: '互联网', salary_min: 12, salary_max: 18 }
])

const careerPath = ref([
  {
    stage: '短期（1-3个月）',
    actions: ['深入学习计算机科学基础', '完成2-3个实战项目', '准备技术面试']
  },
  {
    stage: '中期（3-6个月）',
    actions: ['深入学习Java相关框架', '参与开源项目', '积累项目经验']
  },
  {
    stage: '长期（6-12个月）',
    actions: ['掌握微服务架构', '学习分布式系统', '准备校招投递']
  }
])

const resetMatch = () => {
  matchResult.value = null
  selectedJob.value = null
}
</script>

<style scoped lang="scss">
.career-plan-page {

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

    .profile-info {
      font-size: 0.875rem;
      color: rgba(255, 255, 255, 0.9);
      background: rgba(255, 255, 255, 0.15);
      padding: 0.5rem 1rem;
      border-radius: 8px;
    }
  }
}

.card-title {
  font-weight: 600;
  font-size: 1rem;
}

.card-desc {
  font-size: 0.875rem;
  color: #606266;
  margin-top: 0.25rem;
}

.job-select-area {
  .search-box {
    margin-bottom: 1rem;

    .search-label {
      display: block;
      font-size: 0.875rem;
      font-weight: 500;
      margin-bottom: 0.5rem;
    }
  }
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-bottom: 1rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.job-option {
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    border-color: #409eff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }

  &.selected {
    border-color: #409eff;
    background: #ecf5ff;
    box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
  }

  .job-name {
    font-weight: 500;
    margin-bottom: 0.5rem;
  }

  .job-info {
    p {
      font-size: 0.875rem;
      color: #606266;
      margin-bottom: 0.25rem;

      .label {
        display: inline-block;
        width: 4rem;
      }
    }
  }
}

.match-btn {
  width: 100%;
  margin-top: 1rem;
}

.match-result {
  .profile-summary {
    margin-bottom: 1.5rem;
    background: #ecf5ff;
    border-color: #b3d8ff;

    .summary-title {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: bold;
      margin-bottom: 1rem;
      color: #409eff;
    }

    .summary-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 1rem;
      font-size: 0.875rem;

      @media (max-width: 768px) {
        grid-template-columns: repeat(2, 1fr);
      }

      .label {
        color: #606266;
      }

      .value {
        font-weight: 500;
      }
    }
  }
}

.result-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }

  h4 {
    font-weight: 500;
    margin-bottom: 1rem;
  }
}

.score-section {
  .score-value {
    font-size: 4rem;
    font-weight: bold;
    color: #409eff;
    margin-bottom: 0.5rem;
  }

  .score-desc {
    color: #606266;
  }
}

.radar-section {
  .radar-placeholder {
    height: 200px;
    background: #f5f7fa;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #909399;
  }
}

.career-path {
  .path-item {
    position: relative;
    padding-left: 2rem;
    margin-bottom: 1.5rem;

    &:last-child {
      margin-bottom: 0;
    }
  }

  .path-number {
    position: absolute;
    left: 0;
    top: 0;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #409eff;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    font-weight: bold;
  }

  .path-stage {
    font-weight: 500;
    color: #409eff;
    margin-bottom: 0.5rem;
  }

  .path-actions {
    list-style: none;
    padding-left: 0;

    li {
      font-size: 0.875rem;
      color: #606266;
      padding: 0.25rem 0;
      padding-left: 1rem;
      position: relative;

      &::before {
        content: '●';
        position: absolute;
        left: 0;
        color: #409eff;
        font-size: 0.5rem;
      }
    }
  }
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}
</style>

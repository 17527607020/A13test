<template>
  <div class="job-list-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <el-icon :size="28">
            <Briefcase />
          </el-icon>
        </div>
        <div class="header-info">
          <h1 class="page-title">岗位列表</h1>
          <p class="page-subtitle">探索各类职业岗位，找到适合你的工作机会</p>
        </div>
      </div>
    </div>

    <el-card class="filter-card">
      <div class="filter-row">
        <el-input v-model="keyword" placeholder="搜索岗位名称..." class="search-input" />
        <div class="filter-selects">
          <el-select v-model="selectedIndustry" placeholder="全行业" clearable>
            <el-option v-for="ind in industries" :key="ind" :label="ind" :value="ind" />
          </el-select>
          <el-select v-model="selectedType" placeholder="全类型" clearable>
            <el-option v-for="type in jobTypes" :key="type" :label="type" :value="type" />
          </el-select>
        </div>
      </div>
    </el-card>

    <div class="jobs-list" v-if="jobs.length > 0">
      <el-card v-for="job in jobs" :key="job.id" class="job-card">
        <template #header>
          <span class="job-title">{{ job.name }}</span>
        </template>
        <div class="job-details">
          <p class="detail-item">
            <span class="label">行业：</span>{{ job.industry }}
          </p>
          <p class="detail-item">
            <span class="label">类型：</span>{{ job.type }}
          </p>
          <p class="detail-item">
            <span class="label">薪资：</span>{{ job.salary_min }}-{{ job.salary_max }}K
          </p>
          <p class="detail-item" v-if="job.location">
            <span class="label">地点：</span>{{ job.location }}
          </p>
          <p class="detail-item desc" v-if="job.description">
            {{ job.description }}
          </p>
        </div>
      </el-card>
    </div>

    <el-card v-else class="empty-card">
      <div class="empty-content">
        <p class="empty-text">暂无岗位数据</p>
        <el-button type="primary">创建示例数据</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Briefcase } from '@element-plus/icons-vue'

const keyword = ref('')
const selectedIndustry = ref('')
const selectedType = ref('')

const industries = ['互联网', '金融', 'AI', '教育', '医疗', '制造', '零售']
const jobTypes = ['开发', '产品', '运营', '设计', '测试', '运维']

const jobs = ref([
  {
    id: '1',
    name: 'Java开发工程师',
    type: '开发',
    industry: '互联网',
    salary_min: 10,
    salary_max: 15,
    location: '北京',
    description: '负责后端系统开发，熟悉Java、Spring Boot等框架'
  },
  {
    id: '2',
    name: '产品经理',
    type: '产品',
    industry: '互联网',
    salary_min: 8,
    salary_max: 12,
    location: '上海',
    description: '负责产品规划和需求分析，有互联网产品经验优先'
  },
  {
    id: '3',
    name: '前端开发工程师',
    type: '开发',
    industry: '互联网',
    salary_min: 12,
    salary_max: 18,
    location: '杭州',
    description: '负责前端页面开发，熟悉React、Vue等框架'
  }
])
</script>

<style scoped lang="scss">
.job-list-page {

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
}

.filter-card {
  margin-bottom: 1.5rem;
  border-radius: 16px;
}

.filter-row {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.filter-selects {
  display: flex;
  gap: 0.5rem;
}

.jobs-list {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.job-card {
  border-radius: 12px;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  }

  .job-title {
    font-size: 1.125rem;
    font-weight: 600;
  }
}

.job-details {
  .detail-item {
    font-size: 0.875rem;
    color: #606266;
    margin-bottom: 0.5rem;

    .label {
      font-weight: 500;
    }

    &.desc {
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }
  }
}

.empty-card {
  border-radius: 16px;

  .empty-content {
    text-align: center;
    padding: 2rem 0;
  }

  .empty-text {
    color: #606266;
    margin-bottom: 1rem;
  }
}
</style>

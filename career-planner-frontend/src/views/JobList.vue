<template>
  <div class="job-list-page">
    <h1 class="page-title">岗位列表</h1>

    <el-card class="filter-card">
      <div class="filter-row">
        <el-input
          v-model="keyword"
          placeholder="搜索岗位名称..."
          class="search-input"
        />
        <div class="filter-selects">
          <el-select v-model="selectedIndustry" placeholder="全行业" clearable>
            <el-option
              v-for="ind in industries"
              :key="ind"
              :label="ind"
              :value="ind"
            />
          </el-select>
          <el-select v-model="selectedType" placeholder="全类型" clearable>
            <el-option
              v-for="type in jobTypes"
              :key="type"
              :label="type"
              :value="type"
            />
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
  .page-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
}

.filter-card {
  margin-bottom: 1.5rem;
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

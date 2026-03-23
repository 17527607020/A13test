<template>
  <div class="report-center-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <el-icon :size="28">
            <Folder />
          </el-icon>
        </div>
        <div class="header-info">
          <h1 class="page-title">报告中心</h1>
          <p class="page-subtitle">查看和管理你的职业规划报告</p>
        </div>
      </div>
    </div>

    <!-- 报告列表 -->
    <div v-if="!selectedReport" class="reports-grid">
      <el-card v-for="report in reports" :key="report.id" class="report-card">
        <template #header>
          <div class="report-header">
            <span class="report-title">{{ report.title }}</span>
            <el-tag :type="report.status === 'published' ? 'success' : 'info'" size="small">
              {{ report.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </div>
          <p class="report-date">创建时间：{{ report.created_at }}</p>
        </template>
        <div class="report-actions">
          <el-button size="small" @click="selectedReport = report">查看/编辑</el-button>
          <el-button size="small">导出PDF</el-button>
          <el-button size="small">删除</el-button>
        </div>
      </el-card>
    </div>

    <!-- 报告详情 -->
    <el-card v-else>
      <template #header>
        <div class="detail-header">
          <span class="detail-title">{{ selectedReport.title }}</span>
          <div class="detail-actions">
            <el-button @click="selectedReport = null">返回列表</el-button>
            <el-button type="primary">保存</el-button>
          </div>
        </div>
      </template>

      <div class="report-content">
        <section class="report-section">
          <h3>一、人岗匹配分析</h3>
          <div class="section-content">
            <p>
              根据您的学生画像与目标岗位要求进行对比分析，整体匹配度为
              <strong class="highlight"> 85%</strong>
              。
            </p>
          </div>
        </section>

        <section class="report-section">
          <h3>二、能力维度对比</h3>
          <div class="section-content">
            <ul>
              <li>• 专业技能：80分（良好）</li>
              <li>• 证书匹配：75分（一般）</li>
              <li>• 软技能：90分（优秀）</li>
              <li>• 实习经历：70分（一般）</li>
              <li>• 学习能力：85分（良好）</li>
            </ul>
          </div>
        </section>

        <section class="report-section">
          <h3>三、职业发展路径</h3>
          <div class="section-content">
            <div class="path-item">
              <strong>短期目标（1-3个月）：</strong>
              <p class="path-desc">深入学习Java开发基础，完成2-3个实战项目</p>
            </div>
            <div class="path-item">
              <strong>中期目标（3-6个月）：</strong>
              <p class="path-desc">深入学习Spring框架，参与开源项目积累经验</p>
            </div>
            <div class="path-item">
              <strong>长期目标（6-12个月）：</strong>
              <p class="path-desc">掌握微服务架构，准备校招投递</p>
            </div>
          </div>
        </section>

        <section class="report-section">
          <h3>四、行动建议</h3>
          <div class="section-content">
            <ol>
              <li>重点加强Java核心知识的学习</li>
              <li>积极参与项目实践，积累经验</li>
              <li>考取相关技术证书，提升竞争力</li>
              <li>关注行业动态，了解最新技术趋势</li>
              <li>准备技术面试，练习常见算法题</li>
            </ol>
          </div>
        </section>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Folder } from '@element-plus/icons-vue'

const selectedReport = ref<any>(null)

const reports = ref([
  {
    id: '1',
    title: 'Java开发工程师职业规划报告',
    created_at: '2024-03-08',
    status: 'published'
  },
  {
    id: '2',
    title: '产品经理职业规划报告（草稿）',
    created_at: '2024-03-07',
    status: 'draft'
  }
])
</script>

<style scoped lang="scss">
.report-center-page {

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

.reports-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.report-card {
  .report-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }

  .report-title {
    font-weight: 600;
  }

  .report-date {
    font-size: 0.875rem;
    color: #606266;
  }

  .report-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;

  .detail-title {
    font-weight: 600;
    font-size: 1.125rem;
  }

  .detail-actions {
    display: flex;
    gap: 0.5rem;
  }
}

.report-content {
  .report-section {
    margin-bottom: 1.5rem;

    h3 {
      font-size: 1.125rem;
      font-weight: 500;
      margin-bottom: 0.75rem;
    }

    .section-content {
      background: #f5f7fa;
      padding: 1rem;
      border-radius: 8px;
      color: #606266;

      ul,
      ol {
        padding-left: 1.5rem;
      }

      li {
        margin-bottom: 0.5rem;
      }
    }

    .highlight {
      color: #409eff;
    }

    .path-item {
      margin-bottom: 0.75rem;

      .path-desc {
        margin-left: 1rem;
        color: #606266;
      }
    }
  }
}
</style>

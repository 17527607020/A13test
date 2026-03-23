<template>
  <div class="ability-radar">
    <el-card class="radar-card" shadow="hover">
      <template #header>
        <div class="card-header-content">
          <span class="card-title">能力画像</span>
          <span class="card-subtitle">基于您的信息生成的综合能力评估</span>
        </div>
      </template>

      <div ref="chartRef" class="chart-container"></div>

      <div class="ability-summary" v-if="summary">
        <el-alert :title="summary" type="success" :closable="false" show-icon />
      </div>

      <div class="ability-scores">
        <div class="score-item" v-for="(value, key) in abilityScores" :key="key">
          <div class="score-header">
            <span class="score-label">{{ getAbilityLabel(key) }}</span>
            <span class="score-value" :style="{ color: getScoreColor(value) }">{{ value }}分</span>
          </div>
          <el-progress :percentage="value" :color="getScoreColor(value)" :stroke-width="10" :show-text="false" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import type { AbilityScores } from '@/api/studentProfile'

interface Props {
  abilityScores: AbilityScores
  summary?: string
}

const props = withDefaults(defineProps<Props>(), {
  summary: ''
})

const chartRef = ref<HTMLElement>()
let chart: ECharts | null = null

const abilityLabels = {
  professional_skills: '专业技能',
  learning_ability: '学习能力',
  communication: '沟通能力',
  stress_resistance: '抗压能力',
  innovation: '创新能力',
  internship_ability: '实习能力'
}

const getAbilityLabel = (key: keyof AbilityScores): string => {
  return abilityLabels[key] || key
}

const getScoreColor = (score: number): string => {
  if (score >= 80) return '#6B5CE7'
  if (score >= 60) return '#8A7FE0'
  if (score >= 40) return '#A5A0E8'
  return '#C5C2F0'
}

const initChart = () => {
  if (chartRef.value) {
    if (chart) {
      chart.dispose()
    }
    chart = echarts.init(chartRef.value)
    updateChart()
  }
}

const updateChart = () => {
  if (!chart || !chartRef.value) return

  const values = Object.values(props.abilityScores)
  if (!values || values.length === 0) return

  const option: EChartsOption = {
    radar: {
      indicator: [
        { name: '专业技能', max: 100 },
        { name: '学习能力', max: 100 },
        { name: '沟通能力', max: 100 },
        { name: '抗压能力', max: 100 },
        { name: '创新能力', max: 100 },
        { name: '实习能力', max: 100 }
      ],
      center: ['50%', '50%'],
      radius: '70%',
      splitNumber: 4,
      axisName: {
        color: '#606266',
        fontSize: 14,
        fontWeight: 500
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(107, 92, 231, 0.02)', 'rgba(107, 92, 231, 0.05)', 'rgba(107, 92, 231, 0.08)', 'rgba(107, 92, 231, 0.12)']
        }
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(107, 92, 231, 0.2)'
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(107, 92, 231, 0.3)'
        }
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name: '能力画像',
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 1,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(107, 92, 231, 0.3)' },
              { offset: 1, color: 'rgba(138, 127, 224, 0.5)' }
            ]
          }
        },
        lineStyle: {
          color: '#6B5CE7',
          width: 3
        },
        itemStyle: {
          color: '#6B5CE7',
          borderColor: '#fff',
          borderWidth: 2,
          shadowColor: 'rgba(107, 92, 231, 0.5)',
          shadowBlur: 10
        },
        emphasis: {
          areaStyle: {
            color: 'rgba(107, 92, 231, 0.6)'
          }
        }
      }]
    }],
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e4e7ed',
      borderWidth: 1,
      textStyle: {
        color: '#303133'
      },
      formatter: (params: any) => {
        if (!params || !params.data) return ''
        const data = params.data
        const indicators = ['专业技能', '学习能力', '沟通能力', '抗压能力', '创新能力', '实习能力']
        let html = '<div style="padding: 12px; min-width: 160px;">'
        html += '<div style="font-weight: 600; margin-bottom: 10px; color: #6B5CE7;">能力画像详情</div>'
        indicators.forEach((indicator, index) => {
          const score = data.value[index]
          const color = getScoreColor(score)
          html += `<div style="display: flex; justify-content: space-between; margin: 6px 0; padding: 4px 0; border-bottom: 1px solid #f0f0f0;">
            <span style="color: #606266;">${indicator}</span>
            <span style="font-weight: 600; color: ${color};">${score}</span>
          </div>`
        })
        html += '</div>'
        return html
      }
    }
  }

  try {
    chart.setOption(option)
  } catch (error) {
    console.error('ECharts设置选项失败:', error)
  }
}

watch(() => props.abilityScores, (newScores) => {
  console.log('AbilityScores changed:', newScores)
  if (newScores) {
    setTimeout(() => {
      updateChart()
    }, 100)
  }
}, { deep: true, immediate: true })

onMounted(() => {
  console.log('AbilityRadar mounted, abilityScores:', props.abilityScores)
  setTimeout(() => {
    initChart()
  }, 100)
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped lang="scss">
.ability-radar {
  .radar-card {
    margin-bottom: 1rem;
    border-radius: 16px;
    border: none;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
    }

    :deep(.el-card__header) {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #f0f0f0;
    }

    .card-header-content {
      display: flex;
      flex-direction: column;
      gap: 0.25rem;

      .card-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #303133;
        display: flex;
        align-items: center;
        gap: 0.5rem;

        &::before {
          content: '';
          width: 4px;
          height: 20px;
          background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
          border-radius: 2px;
        }
      }

      .card-subtitle {
        font-size: 0.875rem;
        color: #909399;
        margin-left: 0.75rem;
      }
    }
  }

  .chart-container {
    width: 100%;
    height: 380px;
    margin-bottom: 1.5rem;
  }

  .ability-summary {
    margin-bottom: 1.5rem;

    :deep(.el-alert) {
      border-radius: 10px;
      border: none;
      background: linear-gradient(135deg, #f0f9eb 0%, #e1f3d8 100%);

      .el-alert__icon {
        color: #6B5CE7;
      }

      .el-alert__title {
        color: #606266;
        font-weight: 500;
      }
    }
  }

  .ability-scores {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.25rem;
    padding: 0.5rem 0;

    .score-item {
      background: #fafafa;
      border-radius: 12px;
      padding: 1rem 1.25rem;
      transition: all 0.3s ease;

      &:hover {
        background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
        transform: translateX(4px);
      }

      .score-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.75rem;

        .score-label {
          font-size: 0.95rem;
          color: #606266;
          font-weight: 500;
        }

        .score-value {
          font-size: 1.1rem;
          font-weight: 600;
        }
      }

      :deep(.el-progress) {
        .el-progress-bar__outer {
          background-color: #e4e7ed;
          border-radius: 6px;
        }

        .el-progress-bar__inner {
          border-radius: 6px;
          background: linear-gradient(90deg, #6B5CE7 0%, #8A7FE0 100%);
        }
      }
    }
  }
}
</style>

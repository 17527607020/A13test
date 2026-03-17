<template>
  <div class="ability-radar">
    <el-card class="radar-card">
      <template #header>
        <span class="card-title">能力画像</span>
      </template>
      
      <div ref="chartRef" class="chart-container"></div>
      
      <div class="ability-summary" v-if="summary">
        <el-alert :title="summary" type="success" :closable="false" show-icon />
      </div>
      
      <div class="ability-scores">
        <div class="score-item" v-for="(value, key) in abilityScores" :key="key">
          <span class="score-label">{{ getAbilityLabel(key) }}</span>
          <el-progress 
            :percentage="value" 
            :color="getScoreColor(value)"
            :stroke-width="8"
          />
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
  if (score >= 80) return '#67C23A'
  if (score >= 60) return '#409EFF'
  if (score >= 40) return '#E6A23C'
  return '#F56C6C'
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
        color: '#666',
        fontSize: 14
      }
    },
    series: [{
      type: 'radar',
      data: [{
        value: values,
        name: '能力画像',
        areaStyle: {
          color: 'rgba(103, 194, 58, 0.3)'
        },
        lineStyle: {
          color: '#67C23A',
          width: 2
        },
        itemStyle: {
          color: 'rgba(103, 194, 58, 0.8)',
          borderColor: '#67C23A',
          borderWidth: 2
        },
        emphasis: {
          areaStyle: {
            color: 'rgba(103, 194, 58, 0.6)'
          }
        }
      }]
    }],
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (!params || !params.data) return ''
        const data = params.data
        const indicators = ['专业技能', '学习能力', '沟通能力', '抗压能力', '创新能力', '实习能力']
        let html = '<div style="padding: 10px;">'
        indicators.forEach((indicator, index) => {
          html += `<div style="margin: 5px 0;">${indicator}: <strong>${data.value[index]}</strong></div>`
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
    
    .card-title {
      font-size: 1.2rem;
      font-weight: bold;
      color: #303133;
    }
  }
  
  .chart-container {
    width: 100%;
    height: 400px;
    margin-bottom: 1.5rem;
  }
  
  .ability-summary {
    margin-bottom: 1.5rem;
  }
  
  .ability-scores {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    
    .score-item {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
      
      .score-label {
        font-size: 0.9rem;
        color: #606266;
        font-weight: 500;
      }
    }
  }
}
</style>

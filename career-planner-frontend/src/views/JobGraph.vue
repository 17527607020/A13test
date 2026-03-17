<template>
  <div class="job-graph-page">
    <h1 class="page-title">岗位图谱</h1>

    <el-card class="control-card">
      <div class="control-row">
        <el-select
          v-model="selectedJob"
          placeholder="选择岗位查看图谱"
          clearable
          filterable
          @change="handleJobChange"
          class="job-select"
        >
          <el-option
            v-for="job in jobsWithPaths"
            :key="job.name"
            :label="job.name"
            :value="job.name"
          >
            <span>{{ job.name }}</span>
            <span class="job-info">
              (晋升: {{ job.promotion_count }}, 换岗: {{ job.transfer_count }})
            </span>
          </el-option>
        </el-select>

        <el-radio-group v-model="graphType" @change="handleGraphTypeChange">
          <el-radio-button value="all">全部图谱</el-radio-button>
          <el-radio-button value="promotion">晋升路径</el-radio-button>
          <el-radio-button value="transfer">换岗路径</el-radio-button>
        </el-radio-group>

        <el-button @click="resetGraph" :icon="RefreshRight">重置</el-button>
      </div>
    </el-card>

    <el-card class="graph-card">
      <div ref="chartRef" class="chart-container"></div>
    </el-card>

    <el-dialog v-model="showJobDetail" :title="currentJob?.name" width="500px">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="岗位类型">
          <el-tag :type="getJobTagType(currentJob?.type)">
            {{ getJobTypeLabel(currentJob?.type) }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="薪资范围" v-if="currentJob?.salary">
          {{ currentJob?.salary }}
        </el-descriptions-item>
        <el-descriptions-item label="岗位描述" v-if="currentJob?.description">
          <div class="job-description">{{ currentJob?.description }}</div>
        </el-descriptions-item>
      </el-descriptions>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import type { ECharts, EChartsOption } from 'echarts'
import { RefreshRight } from '@element-plus/icons-vue'
import { jobGraphApi, type JobInfo, type JobNode, type JobLink } from '@/api/jobGraph'

const chartRef = ref<HTMLElement>()
let chart: ECharts | null = null

const jobsWithPaths = ref<JobInfo[]>([])
const selectedJob = ref<string>('')
const graphType = ref<'all' | 'promotion' | 'transfer'>('all')
const showJobDetail = ref(false)
const currentJob = ref<JobNode | null>(null)

const nodeColors: Record<string, string> = {
  '前端开发': '#409EFF',
  '高级前端开发': '#66b1ff',
  '前端架构师': '#a0cfff',
  '大前端技术总监': '#c6e2ff',
  'Java': '#5470C6',
  '高级Java开发': '#7591c6',
  '系统架构师': '#91b4ff',
  'CTO': '#b8d0ff',
  'C/C++': '#91CC75',
  '高级C/C++工程师': '#a8d88f',
  '底层架构师': '#c4e4a8',
  '技术总监': '#ddf0c4',
  '软件测试': '#FAC858',
  '中级测试工程师': '#fbd57a',
  '高级测试工程师': '#fce3a0',
  '测试总监': '#fef1c8',
  '硬件测试': '#EE6666',
  '硬件测试主管': '#f28b8b',
  '硬件质量总监': '#f6b0b0',
  '产品专员/助理': '#73C0DE',
  '初级产品经理': '#8dcfe6',
  '中级产品经理': '#a7ddef',
  '高级产品经理': '#c1eef8',
  '项目经理/主管': '#3BA272',
  '实施工程师': '#5cb88a',
  '高级实施工程师': '#7ecfa2',
  '大区交付总监': '#a0e6ba',
  '技术支持工程师': '#FC8452',
  '高级技术支持': '#fd9c76',
  '客户成功经理': '#feb49a',
  '客户支持总监': '#feccbe',
  'DevOps工程师': '#9A60B4',
  '初级运维工程师': '#ae83c5',
  '中级运维工程师': '#c2a6d6',
  'PMO总监': '#d6c9e7',
  '质量管理/测试': '#EA7CCC',
  '产品经理': '#ee9ca7',
  '测试工程师': '#ffdde1',
  '运维工程师': '#a8e6cf',
  'UI/UX交互设计师': '#dcedc1',
  '交互设计师': '#ffd3b6',
  '大数据开发工程师': '#ffaaa5',
  '嵌入式软件工程师': '#ff8b94',
  '底层驱动开发': '#b8b5ff',
  '自动化测试工程师': '#7868e6',
  '售前咨询顾问': '#ede682',
  '网络客服': '#f6e58d',
  '售前工程师': '#7bed9f',
  '销售运营': '#70a1ff',
  '数据分析师': '#5352ed'
}

const getJobTagType = (type?: string): 'success' | 'primary' | 'warning' => {
  if (type === 'Promotion') return 'success'
  if (type === 'Transfer') return 'warning'
  return 'primary'
}

const getJobTypeLabel = (type?: string): string => {
  if (type === 'Promotion') return '晋升岗位'
  if (type === 'Transfer') return '换岗岗位'
  return '基础岗位'
}

const mockJobs: JobInfo[] = [
  { name: '前端开发', type: '开发', description: '负责前端页面开发', promotion_count: 2, transfer_count: 3 },
  { name: '高级前端开发', type: '开发', description: '负责复杂前端架构', promotion_count: 1, transfer_count: 2 },
  { name: '前端架构师', type: '开发', description: '负责前端技术架构设计', promotion_count: 1, transfer_count: 1 },
  { name: 'Java开发', type: '开发', description: '负责后端Java开发', promotion_count: 2, transfer_count: 2 },
  { name: '高级Java开发', type: '开发', description: '负责复杂后端架构', promotion_count: 1, transfer_count: 2 },
  { name: '系统架构师', type: '开发', description: '负责系统整体架构设计', promotion_count: 1, transfer_count: 1 },
  { name: '软件测试', type: '测试', description: '负责软件测试工作', promotion_count: 2, transfer_count: 2 },
  { name: '中级测试工程师', type: '测试', description: '负责测试用例设计和执行', promotion_count: 1, transfer_count: 2 },
  { name: '高级测试工程师', type: '测试', description: '负责测试架构设计', promotion_count: 1, transfer_count: 1 },
  { name: '产品经理', type: '产品', description: '负责产品规划和需求分析', promotion_count: 2, transfer_count: 2 },
  { name: '高级产品经理', type: '产品', description: '负责复杂产品管理', promotion_count: 1, transfer_count: 1 },
  { name: 'DevOps工程师', type: '运维', description: '负责DevOps相关工作', promotion_count: 1, transfer_count: 2 },
  { name: '运维工程师', type: '运维', description: '负责系统运维工作', promotion_count: 1, transfer_count: 2 }
]

const mockNodes: JobNode[] = [
  { id: '1', name: '前端开发', type: '开发', description: '负责前端页面开发', salary: '10-15K' },
  { id: '2', name: '高级前端开发', type: '开发', description: '负责复杂前端架构', salary: '15-25K' },
  { id: '3', name: '前端架构师', type: '开发', description: '负责前端技术架构设计', salary: '25-40K' },
  { id: '4', name: 'Java开发', type: '开发', description: '负责后端Java开发', salary: '10-18K' },
  { id: '5', name: '高级Java开发', type: '开发', description: '负责复杂后端架构', salary: '18-30K' },
  { id: '6', name: '系统架构师', type: '开发', description: '负责系统整体架构设计', salary: '30-50K' },
  { id: '7', name: '软件测试', type: '测试', description: '负责软件测试工作', salary: '8-12K' },
  { id: '8', name: '中级测试工程师', type: '测试', description: '负责测试用例设计和执行', salary: '12-20K' },
  { id: '9', name: '高级测试工程师', type: '测试', description: '负责测试架构设计', salary: '20-35K' },
  { id: '10', name: '产品经理', type: '产品', description: '负责产品规划和需求分析', salary: '12-20K' },
  { id: '11', name: '高级产品经理', type: '产品', description: '负责复杂产品管理', salary: '20-35K' },
  { id: '12', name: 'DevOps工程师', type: '运维', description: '负责DevOps相关工作', salary: '15-25K' },
  { id: '13', name: '运维工程师', type: '运维', description: '负责系统运维工作', salary: '10-18K' }
]

const mockLinks: JobLink[] = [
  { source: '1', target: '2', type: 'PROMOTES_TO' },
  { source: '2', target: '3', type: 'PROMOTES_TO' },
  { source: '4', target: '5', type: 'PROMOTES_TO' },
  { source: '5', target: '6', type: 'PROMOTES_TO' },
  { source: '7', target: '8', type: 'PROMOTES_TO' },
  { source: '8', target: '9', type: 'PROMOTES_TO' },
  { source: '10', target: '11', type: 'PROMOTES_TO' },
  { source: '13', target: '12', type: 'PROMOTES_TO' },
  { source: '1', target: '7', type: 'TRANSFERS_TO' },
  { source: '1', target: '10', type: 'TRANSFERS_TO' },
  { source: '1', target: '13', type: 'TRANSFERS_TO' },
  { source: '4', target: '7', type: 'TRANSFERS_TO' },
  { source: '4', target: '10', type: 'TRANSFERS_TO' },
  { source: '7', target: '1', type: 'TRANSFERS_TO' },
  { source: '10', target: '1', type: 'TRANSFERS_TO' },
  { source: '10', target: '4', type: 'TRANSFERS_TO' },
  { source: '13', target: '12', type: 'PROMOTES_TO' }
]

const getNodeColor = (jobName: string): string => {
  if (nodeColors[jobName]) {
    return nodeColors[jobName]
  }
  for (const key in nodeColors) {
    if (jobName.includes(key) || key.includes(jobName)) {
      return nodeColors[key]
    }
  }
  const defaultColors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399', '#9A60B4', '#FC8452', '#3BA272']
  let hash = 0
  for (let i = 0; i < jobName.length; i++) {
    hash = hash * 31 + jobName.charCodeAt(i)
  }
  return defaultColors[Math.abs(hash) % defaultColors.length]
}

const initChart = () => {
  if (chartRef.value) {
    chart = echarts.init(chartRef.value)
    chart.on('click', 'series.graph', handleNodeClick)
  }
}

const handleNodeClick = (params: any) => {
  if (params.dataType === 'node') {
    currentJob.value = params.data.value
    showJobDetail.value = true
  }
}

const deduplicateTransferLinks = (links: JobLink[]): JobLink[] => {
  const transferPairs = new Set<string>()
  const result: JobLink[] = []
  
  for (const link of links) {
    if (link.type === 'TRANSFERS_TO') {
      const pairKey = [link.source, link.target].sort().join('-')
      if (!transferPairs.has(pairKey)) {
        transferPairs.add(pairKey)
        result.push(link)
      }
    } else {
      result.push(link)
    }
  }
  
  return result
}

const buildGraphOption = (nodes: JobNode[], links: JobLink[]): EChartsOption => {
  const chartNodes = nodes.map((node) => {
    const color = getNodeColor(node.name)
    const nameLength = node.name.length
    
    let fontSize = 12
    if (nameLength <= 3) {
      fontSize = 14
    } else if (nameLength <= 5) {
      fontSize = 12
    } else if (nameLength <= 7) {
      fontSize = 10
    } else {
      fontSize = 9
    }
    
    return {
      id: node.id,
      name: node.name,
      value: node,
      symbolSize: 60,
      itemStyle: {
        color: color
      },
      label: {
        show: true,
        position: 'inside',
        fontSize: fontSize,
        color: '#000000',
        fontWeight: 600,
        overflow: 'truncate',
        width: 50,
        ellipsis: '...'
      }
    }
  })

  const deduplicatedLinks = deduplicateTransferLinks(links)
  
  const chartLinks = deduplicatedLinks.map(link => ({
    source: link.source,
    target: link.target,
    lineStyle: {
      color: link.type === 'PROMOTES_TO' ? '#67C23A' : '#E6A23C',
      width: 2,
      curveness: 0
    },
    label: {
      show: true,
      formatter: link.type === 'PROMOTES_TO' ? '晋升' : '换岗',
      fontSize: 10,
      color: link.type === 'PROMOTES_TO' ? '#67C23A' : '#E6A23C'
    },
    symbol: link.type === 'PROMOTES_TO' ? ['none', 'arrow'] : ['arrow', 'arrow'],
    symbolSize: [10, 10]
  }))

  return {
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        if (params.dataType === 'node') {
          const data = params.data.value
          return `<strong>${data.name}</strong><br/>
                  类型: ${getJobTypeLabel(data.type)}<br/>
                  ${data.salary ? `薪资: ${data.salary}<br/>` : ''}
                  ${data.description ? `描述: ${data.description.substring(0, 50)}...` : ''}`
        }
        return params.name
      }
    },
    series: [{
      type: 'graph',
      layout: 'force',
      data: chartNodes,
      links: chartLinks,
      roam: true,
      draggable: true,
      force: {
        repulsion: 800,
        edgeLength: [100, 200],
        gravity: 0.05,
        friction: 0.6,
        layoutAnimation: true
      },
      emphasis: {
        focus: 'adjacency',
        lineStyle: {
          width: 4
        }
      },
      edgeSymbol: ['none', 'arrow'],
      edgeSymbolSize: [0, 10]
    }],
    animationDuration: 1500,
    animationEasingUpdate: 'quinticInOut'
  }
}

const loadGraphData = async (useMockFirst: boolean = false) => {
  const showMockData = (nodes: JobNode[], links: JobLink[]) => {
    if (chart && !chart.isDisposed() && nodes.length > 0) {
      const option = buildGraphOption(nodes, links)
      chart.setOption(option, true)
    }
  }
  
  const filterMockData = () => {
    let filteredNodes = mockNodes
    let filteredLinks = mockLinks
    
    if (selectedJob.value) {
      const selectedNode = mockNodes.find(n => n.name === selectedJob.value)
      if (selectedNode) {
        const relatedNodeIds = new Set([selectedNode.id])
        filteredLinks.forEach(link => {
          if (link.source === selectedNode.id) {
            relatedNodeIds.add(link.target)
          } else if (link.target === selectedNode.id) {
            relatedNodeIds.add(link.source)
          }
        })
        
        filteredNodes = mockNodes.filter(n => relatedNodeIds.has(n.id))
        filteredLinks = mockLinks.filter(l => 
          relatedNodeIds.has(l.source) && relatedNodeIds.has(l.target)
        )
        
        if (graphType.value === 'promotion') {
          filteredLinks = filteredLinks.filter(l => l.type === 'PROMOTES_TO')
        } else if (graphType.value === 'transfer') {
          filteredLinks = filteredLinks.filter(l => l.type === 'TRANSFERS_TO')
        }
      }
    } else {
      if (graphType.value === 'promotion') {
        filteredLinks = mockLinks.filter(l => l.type === 'PROMOTES_TO')
      } else if (graphType.value === 'transfer') {
        filteredLinks = mockLinks.filter(l => l.type === 'TRANSFERS_TO')
      }
    }
    
    return { nodes: filteredNodes, links: filteredLinks }
  }
  
  if (useMockFirst) {
    const mockData = filterMockData()
    showMockData(mockData.nodes, mockData.links)
  }
  
  try {
    let data
    if (selectedJob.value) {
      if (graphType.value === 'promotion') {
        data = await jobGraphApi.getPromotionPaths(selectedJob.value)
      } else if (graphType.value === 'transfer') {
        data = await jobGraphApi.getTransferPaths(selectedJob.value)
      } else {
        data = await jobGraphApi.getFullGraph(selectedJob.value, graphType.value)
      }
    } else {
      data = await jobGraphApi.getFullGraph(undefined, graphType.value)
    }

    if (chart && !chart.isDisposed() && data.nodes.length > 0) {
      const option = buildGraphOption(data.nodes, data.links)
      chart.setOption(option, true)
    } else if (chart && !chart.isDisposed()) {
      chart.clear()
      chart.setOption({
        title: {
          text: '暂无图谱数据',
          left: 'center',
          top: 'center'
        }
      })
    }
  } catch (error) {
    console.error('加载图谱数据失败，使用模拟数据:', error)
    const mockData = filterMockData()
    showMockData(mockData.nodes, mockData.links)
  }
}

const handleJobChange = () => {
  loadGraphData(true)
}

const handleGraphTypeChange = () => {
  loadGraphData(true)
}

const resetGraph = () => {
  selectedJob.value = ''
  graphType.value = 'all'
  loadGraphData()
}

const handleResize = () => {
  chart?.resize()
}

onMounted(async () => {
  await nextTick()
  initChart()
  
  try {
    jobsWithPaths.value = await jobGraphApi.getJobsWithPaths()
  } catch (error) {
    console.error('加载岗位列表失败，使用模拟数据:', error)
    jobsWithPaths.value = mockJobs
  }
  
  await loadGraphData(true)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  chart?.dispose()
})
</script>

<style scoped lang="scss">
.job-graph-page {
  .page-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1rem;
  }
}

.control-card {
  margin-bottom: 1rem;
}

.control-row {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.job-select {
  width: 300px;
}

.job-info {
  margin-left: 0.5rem;
  color: #909399;
  font-size: 0.85rem;
}

.graph-card {
  min-height: 600px;
}

.chart-container {
  width: 100%;
  height: 600px;
  cursor: grab;
  
  &:active {
    cursor: grabbing;
  }
}

.job-description {
  max-height: 200px;
  overflow-y: auto;
  line-height: 1.6;
}
</style>

<template>
  <div class="reports-container py-4 text-white">
    <div class="mb-5">
      <h1 class="display-title fw-bold mb-2 text-white glow-text-primary">学习分析报表</h1>
      <p class="text-muted fs-5">深入理解您的学习进展与能力结构。</p>
    </div>

    <!-- Charts Row 1 -->
    <div class="row g-4 mb-4">
      <!-- Capability Radar Chart -->
      <div class="col-lg-6">
        <div class="glass-card chart-card">
          <h4 class="text-white fw-bold mb-3 display-title">五维能力雷达图</h4>
          <p class="text-muted small mb-4">分析词汇、语法、对话、安全、办公五个核心能力的偏向性。</p>
          <div ref="radarChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- Trend Line Chart -->
      <div class="col-lg-6">
        <div class="glass-card chart-card">
          <h4 class="text-white fw-bold mb-3 display-title">近期学习趋势图</h4>
          <p class="text-muted small mb-4">展示最近 14 天您每天获取的经验值与学习时间变化。</p>
          <div ref="trendChartRef" class="chart-container"></div>
        </div>
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="row g-4 mb-4">
      <!-- Department Bar Chart -->
      <div class="col-lg-6">
        <div class="glass-card chart-card">
          <h4 class="text-white fw-bold mb-3 display-title">部门平均成绩对比</h4>
          <p class="text-muted small mb-4">比较公司各部门的平均 XP 积分情况（KPI培训管理参考）。</p>
          <div ref="barChartRef" class="chart-container"></div>
        </div>
      </div>

      <!-- Heatmap Calendar Chart -->
      <div class="col-lg-6">
        <div class="glass-card chart-card">
          <h4 class="text-white fw-bold mb-3 display-title">年度学习热力图</h4>
          <p class="text-muted small mb-4">以日历形式记录您在当前年份里的每日活跃度。</p>
          <div ref="heatmapChartRef" class="chart-container"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const radarChartRef = ref(null)
const trendChartRef = ref(null)
const barChartRef = ref(null)
const heatmapChartRef = ref(null)

let radarChart = null
let trendChart = null
let barChart = null
let heatmapChart = null

const initCharts = (data) => {
  // 1. Radar Chart Configuration
  if (radarChartRef.value) {
    radarChart = echarts.init(radarChartRef.value, 'dark')
    radarChart.setOption({
      backgroundColor: 'transparent',
      tooltip: {},
      radar: {
        indicator: [
          { name: '词汇 (Vocabulary)', max: 100 },
          { name: '语法 (Grammar)', max: 100 },
          { name: '对话 (Dialogue)', max: 100 },
          { name: '安全场景 (Safety)', max: 100 },
          { name: '办公场景 (Work)', max: 100 }
        ],
        splitArea: {
          areaStyle: {
            color: ['rgba(255, 255, 255, 0.02)', 'rgba(255, 255, 255, 0.05)']
          }
        },
        axisLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      },
      series: [{
        name: '能力分值',
        type: 'radar',
        data: [{
          value: [
            data.radar.vocabulary,
            data.radar.grammar,
            data.radar.dialogue,
            data.radar.safety,
            data.radar.work
          ],
          name: '我的水平',
          areaStyle: {
            color: 'rgba(99, 102, 241, 0.3)'
          },
          lineStyle: {
            color: '#6366f1',
            width: 2
          },
          itemStyle: {
            color: '#6366f1'
          }
        }]
      }]
    })
  }

  // 2. Trend Line Chart Configuration
  if (trendChartRef.value) {
    trendChart = echarts.init(trendChartRef.value, 'dark')
    trendChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis' },
      legend: { data: ['经验值 (XP)', '学习时间 (分)'], textStyle: { color: '#9ca3af' } },
      xAxis: {
        type: 'category',
        data: data.trend.dates,
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } }
      },
      yAxis: [
        {
          type: 'value',
          name: '经验',
          axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
          splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
        },
        {
          type: 'value',
          name: '分钟',
          axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
          splitLine: { show: false }
        }
      ],
      series: [
        {
          name: '经验值 (XP)',
          type: 'line',
          smooth: true,
          data: data.trend.xp,
          itemStyle: { color: '#6366f1' },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(99, 102, 241, 0.4)' },
              { offset: 1, color: 'rgba(99, 102, 241, 0)' }
            ])
          }
        },
        {
          name: '学习时间 (分)',
          type: 'line',
          yAxisIndex: 1,
          smooth: true,
          data: data.trend.time,
          itemStyle: { color: '#06b6d4' }
        }
      ]
    })
  }

  // 3. Bar Chart Configuration
  if (barChartRef.value) {
    barChart = echarts.init(barChartRef.value, 'dark')
    barChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'item' },
      xAxis: {
        type: 'category',
        data: data.departments.names,
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
        axisLabel: { interval: 0, rotate: 30 }
      },
      yAxis: {
        type: 'value',
        name: '平均XP',
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.1)' } },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } }
      },
      series: [{
        data: data.departments.scores,
        type: 'bar',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#06b6d4' },
            { offset: 1, color: '#6366f1' }
          ]),
          borderRadius: [6, 6, 0, 0]
        }
      }]
    })
  }

  // 4. Heatmap Chart Configuration
  if (heatmapChartRef.value) {
    heatmapChart = echarts.init(heatmapChartRef.value, 'dark')
    const currentYear = new Date().getFullYear().toString()
    
    heatmapChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { position: 'top' },
      visualMap: {
        min: 0,
        max: 5,
        type: 'piecewise',
        orient: 'horizontal',
        left: 'center',
        top: 0,
        textStyle: { color: '#9ca3af' },
        pieces: [
          { min: 0, max: 0, label: '无活动', color: 'rgba(255, 255, 255, 0.05)' },
          { min: 1, max: 1, label: '1次', color: '#1e1b4b' },
          { min: 2, max: 2, label: '2次', color: '#312e81' },
          { min: 3, max: 3, label: '3次', color: '#4338ca' },
          { min: 4, max: 4, label: '4次', color: '#5850ec' },
          { min: 5, label: '5次及以上', color: '#6366f1' }
        ]
      },
      calendar: {
        top: 60,
        left: 30,
        right: 10,
        range: currentYear,
        cellSize: ['auto', 13],
        itemStyle: {
          borderWidth: 1,
          borderColor: '#111827'
        },
        splitLine: { show: false },
        yearLabel: { show: false },
        dayLabel: { color: '#9ca3af', firstDay: 1, nameMap: ['日', '一', '二', '三', '四', '五', '六'] },
        monthLabel: { color: '#9ca3af', nameMap: 'cn' }
      },
      series: {
        type: 'heatmap',
        coordinateSystem: 'calendar',
        data: data.heatmap
      }
    })
  }
}

const fetchReportData = async () => {
  try {
    const response = await axios.get('/api/reports')
    initCharts(response.data)
  } catch (err) {
    console.error('Failed to load chart coordinates:', err)
  }
}

const handleResize = () => {
  radarChart?.resize()
  trendChart?.resize()
  barChart?.resize()
  heatmapChart?.resize()
}

onMounted(() => {
  fetchReportData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  trendChart?.dispose()
  barChart?.dispose()
  heatmapChart?.dispose()
})
</script>

<style scoped>
.chart-card {
  padding: 24px;
}

.chart-container {
  width: 100%;
  height: 320px;
}
</style>

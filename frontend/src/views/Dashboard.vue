<template>
  <div class="dashboard">
    <!-- Header -->
    <header class="dashboard-header">
      <h1>Data Visualization HeatMap</h1>
      <div class="header-info">
        <span v-if="statistics">
          資料點: {{ statistics.count }} |
          範圍: {{ statistics.minWeight.toFixed(1) }} - {{ statistics.maxWeight.toFixed(1) }}
        </span>
      </div>
    </header>

    <!-- Main content -->
    <div class="dashboard-content" :class="{ 'chat-open': isChatOpen }">
      <!-- Controls section (LEFT SIDE) -->
      <div class="controls-section">
        <!-- Playback Controls -->
        <div class="control-group playback-group">
          <PlaybackControls
            :is-playing="isPlaying"
            :can-play="canPlay"
            :can-pause="canPause"
            :interval-duration="intervalDuration"
            @play="handlePlay"
            @pause="handlePause"
            @reset="handleReset"
          />
        </div>

        <!-- Timeline Slider -->
        <div class="control-group timeline-group">
          <TimelineSlider
            v-model="selectedHourDisplay"
            @change="handleHourChange"
            @input="handleHourInput"
          />
        </div>

        <!-- Month Selection -->
        <div class="control-group month-group">
          <MonthSelector
            v-model="selectedMonth"
            :available-months="monthOptions"
            @change="handleMonthChange"
          />
        </div>

        <!-- Day Type Selection -->
        <div class="control-group daytype-group">
          <DayTypeSelector
            v-model="selectedDayType"
            @change="handleDayTypeChange"
          />
        </div>

        <!-- Metric Selection -->
        <div class="control-group metric-group">
          <MetricSelector
            v-model="selectedMetric"
            :available-metrics="metricOptions"
            @change="handleMetricChange"
          />
        </div>

        <!-- Stats display -->
        <div v-if="statistics" class="stats-card">
          <h3>資料統計</h3>
          <div class="stat-row">
            <span>資料點數:</span>
            <span class="stat-value">{{ statistics.count }}</span>
          </div>
          <div class="stat-row">
            <span>最小值:</span>
            <span class="stat-value">{{ statistics.minWeight.toFixed(2) }}</span>
          </div>
          <div class="stat-row">
            <span>最大值:</span>
            <span class="stat-value">{{ statistics.maxWeight.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Demographics Charts -->
        <div class="charts-section">
          <div class="chart-wrapper">
            <GenderChart
              :data="genderData"
              :loading="demographicsLoading"
              :error="demographicsError"
            />
          </div>
          <div class="chart-wrapper">
            <AgeChart
              :data="ageData"
              :loading="demographicsLoading"
              :error="demographicsError"
            />
          </div>
        </div>
      </div>

      <!-- Map section (RIGHT SIDE) -->
      <div class="map-section">
        <div class="section-header">
          <h2>熱力圖</h2>
          <div class="current-time-display">
            <span class="time-label">當前時間:</span>
            <span class="time-value">{{ currentTimeDisplay }}</span>
          </div>
        </div>

        <!-- Loading and Error Overlay -->
        <div v-show="loading || error" class="overlay-container">
            <div v-if="loading" class="loading-content">
              <div class="spinner"></div>
              <p>載入中...</p>
            </div>
            <div v-else-if="error" class="error-content">
              <p>{{ error }}</p>
              <button @click="initialize" class="btn btn-primary">重試</button>
            </div>
        </div>

        <!-- Map (always rendered) -->
        <HeatmapMap
          :data-points="dataPoints"
          :blur="45"
          :radius="30"
          :min-weight="statistics?.minWeight || 0"
          :max-weight="statistics?.maxWeight || 100"
          @map-ready="onMapReady"
        />
      </div>
    </div>

    <!-- AI Chatbot Sidebar -->
    <ChatSidebar
      :messages="chatMessages"
      :is-thinking="isChatThinking"
      :is-connected="isChatConnected"
      :error="chatError"
      :can-send="canSendMessage"
      @send-message="handleSendMessage"
      @retry="handleRetryMessage"
      @close="handleChatClose"
      @toggle="handleChatToggle"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import HeatmapMap from '../components/map/HeatmapMap.vue'
import PlaybackControls from '../components/controls/PlaybackControls.vue'
import MonthSelector from '../components/controls/MonthSelector.vue'
import MetricSelector from '../components/controls/MetricSelector.vue'
import DayTypeSelector from '../components/controls/DayTypeSelector.vue'
import TimelineSlider from '../components/controls/TimelineSlider.vue'
import GenderChart from '../components/charts/GenderChart.vue'
import AgeChart from '../components/charts/AgeChart.vue'
import ChatSidebar from '../components/chat/ChatSidebar.vue'
import { useHeatmapData } from '../composables/useHeatmapData'
import { useAutoplay } from '../composables/useAutoplay'
import { useDemographics } from '../composables/useDemographics'
import { useChatbot } from '../composables/useChatbot'

// Use heatmap data composable
const {
  loading,
  error,
  dataPoints,
  statistics,
  selectedMonth,
  selectedHour,
  selectedMetric,
  selectedDayType,
  availableMonths,
  availableHours,
  availableMetrics,
  availableDayTypes,
  setHour,
  setDayType,
  initialize
} = useHeatmapData()

// Use autoplay composable
const {
  currentHour: autoplayHour,
  isPlaying,
  canPlay,
  canPause,
  intervalDuration,
  play,
  pause,
  reset,
  setHour: setAutoplayHour
} = useAutoplay(0)

// Use demographics composable (per FR-014: updates with month/hour changes)
const {
  loading: demographicsLoading,
  error: demographicsError,
  genderData,
  ageData
} = useDemographics(selectedMonth, selectedHour, selectedMetric, selectedDayType)

// Sync autoplay hour with heatmap data hour
watch(autoplayHour, (newHour) => {
  setHour(newHour)
})

// Display hour (for select control)
const selectedHourDisplay = computed({
  get: () => selectedHour.value,
  set: (value) => {
    // When user manually changes hour, pause autoplay
    setAutoplayHour(value)
    setHour(value)
  }
})

// Computed
const currentTimeDisplay = computed(() => {
  if (!selectedMonth.value || selectedHour.value === null) return '--'
  return `${formatMonth(selectedMonth.value)} ${formatHour(selectedHour.value)}`
})

// Month options for MonthSelector component
const monthOptions = computed(() => {
  return availableMonths.value.map(month => {
    const year = Math.floor(month / 100)
    const mon = month % 100
    return {
      value: month,
      label: `${year}年${mon}月`,
      sublabel: `${mon}月`
    }
  })
})

// Metric options for MetricSelector component
const metricOptions = computed(() => {
  return availableMetrics.value.map(metric => {
    const labels = {
      'avg_total_users': { label: '全部停留人數', icon: '👥' },
      'avg_users_under_10min': { label: '停留10分鐘以下', icon: '🔵' },
      'avg_users_10_30min': { label: '停留10-30分鐘', icon: '🟡' },
      'avg_users_over_30min': { label: '停留30分鐘以上', icon: '🔴' }
    }
    return {
      value: metric.key,
      label: labels[metric.key]?.label || metric.label,
      icon: labels[metric.key]?.icon || '📊'
    }
  })
})

// Methods
function formatMonth(month) {
  const year = Math.floor(month / 100)
  const mon = month % 100
  return `${year}年${mon}月`
}

function formatHour(hour) {
  return `${hour.toString().padStart(2, '0')}:00`
}

function handlePlay() {
  play()
}

function handlePause() {
  pause()
}

function handleReset() {
  reset()
  setHour(0)
}

function handleMonthChange() {
  // Pause autoplay when user manually changes month (per FR-009)
  pause()
}

function handleHourChange() {
  // Pause autoplay when user manually changes hour via slider (per FR-009)
  pause()
}

function handleHourInput(hour) {
  // Update hour in real-time as slider moves (for smooth UX)
  setAutoplayHour(hour)
}

function handleMetricChange() {
  // Pause autoplay when user manually changes metric (per FR-009)
  pause()
}

function handleDayTypeChange() {
  // Pause autoplay when user manually changes day type
  pause()
}

function onMapReady(mapInstance) {
  console.log('Map ready:', mapInstance)
}

// Use chatbot composable
const heatmapDataForChat = {
  selectedMonth,
  selectedHour,
  selectedDayType
}

const {
  messages: chatMessages,
  isThinking: isChatThinking,
  isConnected: isChatConnected,
  error: chatError,
  canSend: canSendMessage,
  sendMessage: sendChatMessage,
  retryLastMessage,
  stopHealthCheck
} = useChatbot(heatmapDataForChat)

// Chatbot state
const isChatOpen = ref(true)  // 預設開啟

// Chatbot handlers
function handleSendMessage(message) {
  sendChatMessage(message)
}

function handleRetryMessage() {
  retryLastMessage()
}

function handleChatClose() {
  isChatOpen.value = false
}

function handleChatToggle(isOpen) {
  isChatOpen.value = isOpen
}

// Lifecycle
onMounted(() => {
  initialize()
})

onUnmounted(() => {
  // Stop chatbot health check polling on unmount
  stopHealthCheck()
})
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-color);
}

.dashboard-header {
  background: white;
  padding: 16px 24px;
  box-shadow: var(--shadow-sm);
  z-index: 10;
}

.dashboard-header h1 {
  font-size: 1.5rem;
  margin: 0 0 8px 0;
  color: var(--text-primary);
}

.header-info {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.dashboard-content {
  flex: 1;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 16px;
  padding: 16px;
  overflow: hidden;
  transition: margin-right 0.3s ease-in-out;
}

/* 當聊天框開啟時，為地圖留出空間（桌面版） */
@media (min-width: 1024px) {
  .dashboard-content.chat-open {
    margin-right: 350px;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .dashboard-content.chat-open {
    margin-right: 320px;
  }
}

.map-section {
  position: relative;
  background: white;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid var(--border-color);
}

.section-header h2 {
  font-size: 1.125rem;
  margin: 0;
}

.current-time-display {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.875rem;
}

.time-label {
  color: var(--text-secondary);
}

.time-value {
  color: var(--primary-color);
  font-weight: 600;
  font-size: 1rem;
}

.overlay-container {
  position: absolute;
  top: 57px; /* Height of .section-header */
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  backdrop-filter: blur(2px);
}

.loading-content, .error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.error-content {
  color: var(--error-color);
}

.controls-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
  overflow-y: auto;
}

.control-group {
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.control-group label {
  display: block;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--text-primary);
}

.playback-group {
  border: 2px solid var(--primary-color);
}

.timeline-group {
  background: #f9fafb;
  padding: 0;
}

.month-group,
.metric-group,
.daytype-group {
  padding: 12px;
}

.stats-card {
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: var(--shadow-sm);
}

.stats-card h3 {
  font-size: 1rem;
  margin: 0 0 12px 0;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color);
}

.stat-row:last-child {
  border-bottom: none;
}

.stat-value {
  font-weight: 600;
  color: var(--primary-color);
}

.charts-section {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

.chart-wrapper {
  min-height: 300px;
}

/* Responsive design */
@media (max-width: 1023px) {
  .dashboard-content {
    grid-template-columns: 1fr;
    grid-template-rows: 60vh auto;
  }
}

@media (max-width: 767px) {
  .dashboard-header {
    padding: 12px 16px;
  }

  .dashboard-header h1 {
    font-size: 1.25rem;
  }

  .dashboard-content {
    padding: 12px;
    gap: 12px;
  }

  .controls-section {
    flex-direction: row;
    overflow-x: auto;
    flex-wrap: wrap;
  }

  .control-group {
    flex: 1;
    min-width: 150px;
  }

  .playback-group {
    flex: 1 1 100%;
  }
}
</style>

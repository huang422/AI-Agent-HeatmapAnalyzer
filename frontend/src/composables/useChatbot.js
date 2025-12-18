/**
 * useChatbot Composable
 * Manages chatbot state, API communication, and conversation history
 */

import { ref, computed } from 'vue'
import apiClient from '../services/api'

export function useChatbot(heatmapData = null) {
  // State
  const messages = ref([
    {
      id: Date.now(),
      role: 'assistant',
      content: '您好！我是Tangkoco，會深入分析當前熱力圖數據並給出具體、詳細的洞察。\n\n您可以詢問以下類型的問題：\n\n📊 **人流分析**\n• 當前時段有多少使用者？\n• 哪些地點人流最多？\n• 人流最高的前5個位置在哪裡？\n\n👥 **人群分析**\n• 年輕人（20-34歲）主要在哪些區域活動？\n• 男女比例如何？哪些區域女性比例較高？\n• 主要的年齡層是哪些？\n\n⏰ **停留時間**\n• 使用者平均停留多久？\n• 長時間停留（>30分鐘）的地點有哪些？\n\n📍 **地理分佈**\n• 人流集中在哪個區域？\n• 最繁忙的地點座標是什麼？\n\n請隨時提問，我會根據實際數據給您詳細的分析！',
      timestamp: Date.now()
    }
  ])
  const isThinking = ref(false)
  const isConnected = ref(false)
  const error = ref(null)

  // Computed
  const canSend = computed(() => !isThinking.value && isConnected.value)

  /**
   * Get current heatmap context from heatmapData composable
   */
  function getCurrentContext() {
    if (!heatmapData) {
      return {
        month: 202412,
        hour: 0,
        day_type: '平日'
      }
    }

    return {
      month: heatmapData.selectedMonth.value,
      hour: heatmapData.selectedHour.value,
      day_type: heatmapData.selectedDayType.value
    }
  }

  /**
   * Check Ollama service health
   */
  async function checkHealth() {
    try {
      const response = await apiClient.get('/chat/health')
      isConnected.value = response.ollama_status === 'connected' && response.model_loaded
      error.value = response.error
      return response
    } catch (err) {
      console.error('Health check failed:', err)
      isConnected.value = false
      error.value = 'Cannot connect to AI service'
      return null
    }
  }

  /**
   * Send message to AI chatbot
   * @param {string} userMessage - User's question
   */
  async function sendMessage(userMessage) {
    if (!userMessage.trim()) {
      return
    }

    // Validate message length
    if (userMessage.length > 500) {
      error.value = '訊息長度超過 500 字元限制'
      return
    }

    // Add user message to history
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: userMessage.trim(),
      timestamp: Date.now()
    }
    messages.value.push(userMsg)

    // Clear any previous errors
    error.value = null
    isThinking.value = true

    try {
      // Get current heatmap context
      const context = getCurrentContext()

      // Prepare conversation history (last 10 message pairs = 20 messages)
      const history = messages.value
        .filter(m => m.role !== 'system')
        .slice(-20)
        .map(m => ({
          role: m.role,
          content: m.content,
          timestamp: m.timestamp
        }))

      // Call chat API with 30s timeout
      const response = await apiClient.post(
        '/chat/message',
        {
          message: userMessage.trim(),
          context: context,
          history: history
        },
        {
          timeout: 30000
        }
      )

      // Add AI response to messages
      const aiMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp,
        model: response.model,
        tokens: response.tokens_used
      }
      messages.value.push(aiMsg)

    } catch (err) {
      console.error('Failed to send message:', err)

      // Handle different error types
      let errorMessage = '發送訊息失敗，請重試'

      if (err.response) {
        // Server responded with error
        if (err.response.status === 503) {
          errorMessage = '⚠ AI 服務離線，請確認 Ollama 已啟動'
          isConnected.value = false
        } else if (err.response.status === 500) {
          errorMessage = 'AI 推理失敗，請重試或簡化問題'
        } else if (err.response.status === 400) {
          errorMessage = '請求格式錯誤：' + (err.response.data?.detail || '未知錯誤')
        }
      } else if (err.code === 'ECONNABORTED' || err.message.includes('timeout')) {
        errorMessage = '回應超時（30秒），請重試或簡化問題'
      } else if (err.message.includes('Network Error')) {
        errorMessage = '網路連接失敗，請檢查後端服務是否運行'
      }

      error.value = errorMessage

      // Add error message to chat
      messages.value.push({
        id: Date.now() + 1,
        role: 'assistant',
        content: `❌ ${errorMessage}`,
        timestamp: Date.now(),
        isError: true
      })

    } finally {
      isThinking.value = false
    }
  }

  /**
   * Clear conversation history
   */
  function clearMessages() {
    messages.value = [
      {
        id: Date.now(),
        role: 'assistant',
        content: '對話已清除。您可以繼續提問關於熱力圖數據的問題。',
        timestamp: Date.now()
      }
    ]
    error.value = null
  }

  /**
   * Retry last failed message
   */
  function retryLastMessage() {
    // Find last user message
    const lastUserMessage = [...messages.value]
      .reverse()
      .find(m => m.role === 'user')

    if (lastUserMessage) {
      // Remove last AI error message if exists
      if (messages.value[messages.value.length - 1].isError) {
        messages.value.pop()
      }

      sendMessage(lastUserMessage.content)
    }
  }

  // Initialize: check health on mount
  checkHealth()

  // Set up periodic health check (every 30 seconds)
  let healthCheckInterval = null
  const startHealthCheck = () => {
    if (healthCheckInterval) return
    healthCheckInterval = setInterval(() => {
      if (!isConnected.value) {
        checkHealth()
      }
    }, 30000)
  }

  const stopHealthCheck = () => {
    if (healthCheckInterval) {
      clearInterval(healthCheckInterval)
      healthCheckInterval = null
    }
  }

  startHealthCheck()

  return {
    // State
    messages,
    isThinking,
    isConnected,
    error,

    // Computed
    canSend,

    // Methods
    sendMessage,
    checkHealth,
    clearMessages,
    retryLastMessage,
    getCurrentContext,
    startHealthCheck,
    stopHealthCheck
  }
}

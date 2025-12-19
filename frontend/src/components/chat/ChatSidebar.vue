<template>
  <div class="chat-container">
    <!-- Toggle Button -->
    <button
      class="chat-toggle-button"
      @click="toggleSidebar"
      :aria-label="isOpen ? '隱藏聊天機器人' : '顯示聊天機器人'"
      :title="isOpen ? '隱藏聊天機器人' : '顯示聊天機器人'"
    >
      <span class="chat-icon">🐭</span>
      <span v-if="unreadCount > 0 && !isOpen" class="unread-badge">{{ unreadCount }}</span>
    </button>

    <!-- Backdrop (mobile only) -->
    <div
      v-if="isOpen"
      class="chat-backdrop"
      @click="closeSidebar"
      role="button"
      tabindex="0"
      @keydown.enter="closeSidebar"
      @keydown.space="closeSidebar"
    ></div>

    <!-- Sidebar -->
    <div
      :class="['chat-sidebar', { 'is-open': isOpen }]"
      role="complementary"
      aria-label="AI聊天機器人側邊欄"
    >
      <!-- Header -->
      <div class="chat-header">
        <div class="chat-title">
          <span>AI Agent Tangkoco</span>
        </div>
        <div class="chat-header-actions">
          <!-- Connection Status -->
          <span
            :class="['connection-status', isConnected ? 'connected' : 'disconnected']"
            :title="isConnected ? 'AI服務已連線' : 'AI服務離線'"
          >
            <span class="status-indicator">●</span>
            <span class="status-text">{{ isConnected ? '已連線' : '離線' }}</span>
          </span>
          <!-- Close Button -->
          <button
            class="close-button"
            @click="closeSidebar"
            aria-label="關閉側邊欄"
            title="關閉側邊欄"
          >
            ✕
          </button>
        </div>
      </div>

      <!-- Messages Container -->
      <div ref="messagesContainer" class="chat-messages">
        <div
          v-for="message in messages"
          :key="message.id"
          :class="['message', `message-${message.role}`, { 'message-error': message.isError }]"
        >
          <div class="message-content">
            <div class="message-text" v-html="formatMessage(message.content)"></div>
            <div class="message-timestamp">
              {{ formatTimestamp(message.timestamp) }}
            </div>
          </div>
        </div>

        <!-- Thinking Indicator -->
        <div v-if="isThinking" class="message message-assistant thinking">
          <div class="message-content">
            <div class="thinking-dots">
              <span></span><span></span><span></span>
            </div>
            <div class="message-timestamp">AI 分析中...</div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="chat-input-container">
        <!-- Error Display -->
        <div v-if="error" class="error-banner">
          <span>{{ error }}</span>
          <button @click="retryLastMessage" class="retry-button" title="重試">
            ↻ 重試
          </button>
        </div>

        <!-- Input Form -->
        <form @submit.prevent="handleSend" class="chat-input-form">
          <input
            ref="inputField"
            v-model="inputMessage"
            type="text"
            placeholder="Ask Tangkoco"
            :disabled="!canSend"
            :maxlength="500"
            class="chat-input"
            aria-label="聊天訊息輸入框"
            @keydown.enter.exact.prevent="handleSend"
            @keydown.escape="closeSidebar"
          />
          <div class="input-actions">
            <span class="char-count" :class="{ 'limit-warning': inputMessage.length > 450 }">
              {{ inputMessage.length }}/500
            </span>
            <button
              type="submit"
              class="send-button"
              :disabled="!canSend || !inputMessage.trim()"
              aria-label="發送訊息"
              title="發送訊息 (Enter)"
            >
              ➤
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, nextTick, onUnmounted } from 'vue'

export default {
  name: 'ChatSidebar',
  props: {
    messages: {
      type: Array,
      required: true
    },
    isThinking: {
      type: Boolean,
      default: false
    },
    isConnected: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    },
    canSend: {
      type: Boolean,
      default: true
    }
  },
  emits: ['send-message', 'retry', 'close', 'toggle'],
  setup(props, { emit }) {
    // 根據螢幕寬度決定預設狀態：桌面版開啟，手機/平板關閉
    const getInitialOpenState = () => {
      if (typeof window === 'undefined') return false
      return window.innerWidth > 1023
    }

    const isOpen = ref(getInitialOpenState())
    const inputMessage = ref('')
    const messagesContainer = ref(null)
    const inputField = ref(null)
    const unreadCount = ref(0)

    // Toggle sidebar
    function toggleSidebar() {
      isOpen.value = !isOpen.value
      emit('toggle', isOpen.value)  // 發出切換事件
      if (isOpen.value) {
        unreadCount.value = 0
        nextTick(() => {
          scrollToBottom()
          inputField.value?.focus()
        })
      }
    }

    // 初始化時，如果是桌面版且開啟，則聚焦和滾動
    nextTick(() => {
      if (isOpen.value) {
        scrollToBottom()
        inputField.value?.focus()
      }
    })

    function closeSidebar() {
      isOpen.value = false
      emit('toggle', false)  // 發出切換事件
      emit('close')
    }

    // Handle message send
    function handleSend() {
      if (!props.canSend || !inputMessage.value.trim()) {
        return
      }

      emit('send-message', inputMessage.value)
      inputMessage.value = ''

      // Scroll to bottom after sending
      nextTick(() => {
        scrollToBottom()
      })
    }

    // Retry last message
    function retryLastMessage() {
      emit('retry')
    }

    // Auto-scroll to bottom when new messages arrive
    function scrollToBottom() {
      if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
      }
    }

    // Watch for new messages
    watch(
      () => props.messages.length,
      (newLength, oldLength) => {
        if (newLength > oldLength) {
          // New message arrived
          if (!isOpen.value && newLength > 1) {
            // Increment unread count if sidebar is closed (skip initial welcome message)
            unreadCount.value++
          }

          // Auto-scroll if sidebar is open
          if (isOpen.value) {
            nextTick(() => {
              scrollToBottom()
            })
          }
        }
      }
    )

    // Format timestamp
    function formatTimestamp(timestamp) {
      if (!timestamp) return ''
      const date = new Date(timestamp)
      return date.toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' })
    }

    // Format message content (convert newlines to <br>)
    function formatMessage(content) {
      return content.replace(/\n/g, '<br>')
    }

    // Keyboard shortcuts
    function handleKeyboard(event) {
      // Escape to close
      if (event.key === 'Escape' && isOpen.value) {
        closeSidebar()
      }
    }

    // Add keyboard listener
    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', handleKeyboard)
    }

    onUnmounted(() => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('keydown', handleKeyboard)
      }
    })

    return {
      isOpen,
      inputMessage,
      messagesContainer,
      inputField,
      unreadCount,
      toggleSidebar,
      closeSidebar,
      handleSend,
      retryLastMessage,
      scrollToBottom,
      formatTimestamp,
      formatMessage
    }
  }
}
</script>

<style scoped>
/* Chat Container */
.chat-container {
  position: relative;
  z-index: 100;
}

/* Toggle Button */
.chat-toggle-button {
  position: fixed;
  right: 20px;
  top: 80px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  z-index: 101;
}

.chat-toggle-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}

.chat-icon {
  font-size: 28px;
}

.unread-badge {
  position: absolute;
  top: 5px;
  right: 5px;
  background: #ff4444;
  color: white;
  font-size: 12px;
  font-weight: bold;
  padding: 2px 6px;
  border-radius: 10px;
  min-width: 20px;
  text-align: center;
}

/* Backdrop (mobile) */
.chat-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
  display: none;
}

/* Sidebar */
.chat-sidebar {
  position: fixed;
  right: 0;
  top: 0;
  bottom: 0;
  width: 350px;
  background: white;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
  display: flex;
  flex-direction: column;
  z-index: 100;
}

.chat-sidebar.is-open {
  transform: translateX(0);
}

/* Header */
.chat-header {
  padding: 16px;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 16px;
}

.chat-header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.status-indicator {
  font-size: 10px;
}

.connection-status.connected .status-indicator {
  color: #4caf50;
}

.connection-status.disconnected .status-indicator {
  color: #ff9800;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-button:hover {
  opacity: 1;
}

/* Messages */
.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: #f5f5f5;
}

.message {
  margin-bottom: 16px;
  display: flex;
}

.message-user {
  justify-content: flex-end;
}

.message-content {
  max-width: 80%;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.4;
}

.message-user .message-content {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message-assistant .message-content {
  background: white;
  color: #333;
  border-bottom-left-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-error .message-content {
  background: #ffebee;
  color: #c62828;
  border-left: 3px solid #f44336;
}

.message-text {
  margin-bottom: 4px;
}

.message-timestamp {
  font-size: 11px;
  opacity: 0.7;
  text-align: right;
}

/* Thinking Indicator */
.thinking .message-content {
  background: white;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.thinking-dots {
  display: flex;
  gap: 4px;
}

.thinking-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #667eea;
  animation: thinking 1.4s infinite ease-in-out both;
}

.thinking-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.thinking-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes thinking {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Input Area */
.chat-input-container {
  border-top: 1px solid #e0e0e0;
  background: white;
}

.error-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: #ffebee;
  color: #c62828;
  font-size: 13px;
  border-bottom: 1px solid #ffcdd2;
}

.retry-button {
  background: none;
  border: 1px solid #c62828;
  color: #c62828;
  padding: 4px 8px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.retry-button:hover {
  background: #c62828;
  color: white;
}

.chat-input-form {
  padding: 12px;
}

.chat-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  font-family: inherit;
}

.chat-input:focus {
  border-color: #667eea;
}

.chat-input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.char-count {
  font-size: 12px;
  color: #999;
}

.char-count.limit-warning {
  color: #ff9800;
  font-weight: 600;
}

.send-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 16px;
  transition: opacity 0.2s;
}

.send-button:hover:not(:disabled) {
  opacity: 0.9;
}

.send-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Responsive Design */
@media (max-width: 1023px) {
  .chat-sidebar {
    width: 320px;
  }

  .chat-toggle-button {
    width: 52px;
    height: 52px;
    top: 76px;
  }

  .chat-icon {
    font-size: 24px;
  }
}

@media (max-width: 767px) {
  .chat-backdrop {
    display: block;
  }

  .chat-sidebar {
    width: 100vw;
    max-width: 100%;
  }

  .chat-messages {
    padding: 12px;
  }

  .message-content {
    max-width: 90%;
  }

  .chat-toggle-button {
    top: 70px;
    right: 12px;
    width: 48px;
    height: 48px;
  }

  .chat-icon {
    font-size: 20px;
  }

  .unread-badge {
    top: 2px;
    right: 2px;
    font-size: 10px;
    padding: 1px 4px;
    min-width: 16px;
  }

  .chat-input-form {
    padding: 10px;
  }

  .chat-input {
    padding: 8px 10px;
    font-size: 14px;
  }

  .send-button {
    padding: 6px 12px;
    font-size: 14px;
  }
}
</style>

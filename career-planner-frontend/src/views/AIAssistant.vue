<template>
  <div class="ai-assistant-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <el-icon :size="28">
            <ChatDotRound />
          </el-icon>
        </div>
        <div class="header-info">
          <h1 class="page-title">AI职业规划助手</h1>
          <p class="page-subtitle">专业的职业规划智能体，帮助你找到最适合的职业发展路径</p>
        </div>
      </div>
    </div>

    <!-- 聊天区域 -->
    <el-card class="chat-card">
      <div class="chat-messages">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <div class="message-content">
            {{ message.content }}
          </div>
        </div>
        <div v-if="isLoading" class="message assistant">
          <div class="loading-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 快捷问题 -->
    <div v-if="messages.length === 1" class="quick-questions">
      <p class="quick-label">常见问题：</p>
      <div class="quick-buttons">
        <el-button v-for="(question, index) in quickQuestions" :key="index" size="small"
          @click="handleQuickQuestion(question)">
          {{ question }}
        </el-button>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="input-area">
      <el-input v-model="input" placeholder="输入你的问题..." @keypress.enter="handleSend" :disabled="isLoading" />
      <el-button type="primary" @click="handleSend" :disabled="isLoading || !input.trim()">
        发送
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const input = ref('')
const isLoading = ref(false)

const messages = ref<Message[]>([
  {
    role: 'assistant',
    content:
      '你好！我是你的职业规划助手 👋\n\n我可以帮你：\n• 分析职业发展方向 🔍\n• 推荐适合的岗位 💼\n• 制定学习计划 📚\n\n请问有什么可以帮助你？'
  }
])

const quickQuestions = ref([
  '如何选择职业方向？',
  'Java开发需要哪些技能？',
  '如何准备面试？',
  '在校期间做什么准备？'
])

const handleSend = () => {
  if (!input.value.trim() || isLoading.value) return

  messages.value.push({
    role: 'user',
    content: input.value
  })

  input.value = ''
  isLoading.value = true

  // 模拟回复
  setTimeout(() => {
    messages.value.push({
      role: 'assistant',
      content: '这是一个模拟的AI回复。在实际项目中，这里会调用AI API获取回复。'
    })
    isLoading.value = false
  }, 1000)
}

const handleQuickQuestion = (question: string) => {
  input.value = question
  handleSend()
}
</script>

<style scoped lang="scss">
.ai-assistant-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 200px);

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

.chat-card {
  flex: 1;
  overflow: hidden;
  margin-bottom: 1rem;

  :deep(.el-card__body) {
    height: 100%;
    padding: 1rem;
    overflow-y: auto;
  }
}

.chat-messages {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;

  &.user {
    justify-content: flex-end;

    .message-content {
      background: #409eff;
      color: white;
    }
  }

  &.assistant {
    justify-content: flex-start;

    .message-content {
      background: #f5f7fa;
      color: #303133;
    }
  }

  .message-content {
    max-width: 80%;
    padding: 1rem;
    border-radius: 8px;
    white-space: pre-wrap;
  }
}

.loading-dots {
  display: flex;
  gap: 4px;
  padding: 1rem;
  background: #f5f7fa;
  border-radius: 8px;

  span {
    width: 8px;
    height: 8px;
    background: #c0c4cc;
    border-radius: 50%;
    animation: bounce 1.4s infinite ease-in-out both;

    &:nth-child(1) {
      animation-delay: -0.32s;
    }

    &:nth-child(2) {
      animation-delay: -0.16s;
    }
  }
}

@keyframes bounce {

  0%,
  80%,
  100% {
    transform: scale(0);
  }

  40% {
    transform: scale(1);
  }
}

.quick-questions {
  margin-bottom: 1rem;

  .quick-label {
    font-size: 0.875rem;
    color: #606266;
    margin-bottom: 0.5rem;
  }

  .quick-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
}

.input-area {
  display: flex;
  gap: 0.5rem;

  :deep(.el-input) {
    flex: 1;
  }
}
</style>

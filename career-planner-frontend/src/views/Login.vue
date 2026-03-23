<template>
  <div class="login-page">
    <div class="login-container">
      <!-- 左侧 - 平台介绍 -->
      <div class="intro-section">
        <h1 class="intro-title">
          基于AI的
          <br />
          大学生职业规划智能体
        </h1>
        <p class="intro-desc">
          基于大语言模型与职业大数据的
          <br />
          新一代大学生职业发展智能服务平台
        </p>

        <!-- 核心功能 -->
        <div class="features">
          <div class="feature-item">
            <div class="feature-icon">
              <el-icon>
                <TrendCharts />
              </el-icon>
            </div>
            <div class="feature-content">
              <p class="feature-title">AI职业测评</p>
              <p class="feature-desc">智能分析兴趣、能力与性格，生成专属职业画像</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <el-icon>
                <Opportunity />
              </el-icon>
            </div>
            <div class="feature-content">
              <p class="feature-title">智能规划方案</p>
              <p class="feature-desc">结合行业趋势，生成个性化职业发展路径</p>
            </div>
          </div>

          <div class="feature-item">
            <div class="feature-icon">
              <el-icon>
                <ChatDotRound />
              </el-icon>
            </div>
            <div class="feature-content">
              <p class="feature-title">导师在线咨询</p>
              <p class="feature-desc">连接行业导师，获取专业职业指导</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧 - 表单 -->
      <div class="form-section">
        <div class="form-wrapper">
          <div class="form-header">
            <h2 class="form-title">{{ isLogin ? '欢迎回来' : '创建账号' }}</h2>
            <p class="form-subtitle">
              {{ isLogin ? '请登录您的账号以继续' : '开始您的职业规划之旅' }}
            </p>
          </div>

          <el-alert v-if="error" :title="error" type="error" :closable="false" show-icon class="error-alert" />

          <el-form @submit.prevent="handleSubmit" class="login-form">
            <el-form-item>
              <el-input v-model="formData.username" placeholder="用户名" size="large" />
            </el-form-item>

            <el-form-item v-if="!isLogin">
              <el-input v-model="formData.email" type="email" placeholder="邮箱" size="large" />
            </el-form-item>

            <el-form-item>
              <el-input v-model="formData.password" type="password" placeholder="密码" size="large" show-password />
            </el-form-item>

            <el-form-item v-if="!isLogin">
              <el-input v-model="formData.confirmPassword" type="password" placeholder="确认密码" size="large"
                show-password />
            </el-form-item>

            <el-button type="primary" native-type="submit" size="large" class="submit-btn" :loading="loading">
              {{ loading ? '处理中...' : isLogin ? '登录' : '注册' }}
            </el-button>
          </el-form>

          <!-- 角色选择 -->
          <div v-if="!isLogin" class="role-select">
            <p class="role-label">选择角色</p>
            <div class="role-options">
              <div v-for="role in roles" :key="role.value"
                :class="['role-option', { active: selectedRole === role.value }]" @click="selectedRole = role.value">
                <el-icon :size="20">
                  <component :is="role.icon" />
                </el-icon>
                <span>{{ role.label }}</span>
              </div>
            </div>
          </div>

          <div class="switch-mode">
            <el-button type="primary" link @click="isLogin = !isLogin">
              {{ isLogin ? '还没有账号？立即注册' : '已有账号？立即登录' }}
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { TrendCharts, Opportunity, ChatDotRound, User, Reading, Setting } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const isLogin = ref(true)
const loading = ref(false)
const error = ref('')
const selectedRole = ref<'student' | 'mentor' | 'admin'>('student')

const formData = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const roles = [
  { value: 'student' as const, label: '学生', icon: User },
  { value: 'mentor' as const, label: '导师', icon: Reading },
  { value: 'admin' as const, label: '管理', icon: Setting }
]

const handleSubmit = async () => {
  error.value = ''
  loading.value = true

  try {
    if (isLogin.value) {
      // 登录
      await userStore.login({
        username: formData.value.username,
        password: formData.value.password
      })
      ElMessage.success('登录成功')
      // 使用 window.location 强制刷新页面，确保 localStorage 已更新
      window.location.href = '/'
    } else {
      // 注册
      if (formData.value.password !== formData.value.confirmPassword) {
        error.value = '两次输入的密码不一致'
        loading.value = false
        return
      }

      await userStore.register({
        username: formData.value.username,
        email: formData.value.email,
        password: formData.value.password,
        role: selectedRole.value
      })
      ElMessage.success('注册成功')
      window.location.href = '/'
    }
  } catch (err: any) {
    error.value = err.message || (isLogin.value ? '登录失败' : '注册失败')
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  padding: 1rem;
}

.login-container {
  width: 100%;
  max-width: 900px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;

  @media (min-width: 768px) {
    flex-direction: row;
  }
}

.intro-section {
  flex: 1;
  background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
  padding: 2rem;

  @media (min-width: 768px) {
    padding: 3rem;
  }
}

.intro-title {
  font-size: 1.75rem;
  font-weight: bold;
  color: #fff;
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.intro-desc {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.875rem;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.feature-item {
  display: flex;
  gap: 0.75rem;
}

.feature-icon {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 2px;
}

.feature-content {
  .feature-title {
    font-weight: 500;
    color: #fff;
    margin-bottom: 0.125rem;
  }

  .feature-desc {
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.8);
  }
}

.form-section {
  flex: 1;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;

  @media (min-width: 768px) {
    padding: 3rem;
  }
}

.form-wrapper {
  width: 100%;
  max-width: 360px;
}

.form-header {
  text-align: center;
  margin-bottom: 2rem;

  .form-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: #303133;
    margin-bottom: 0.25rem;
  }

  .form-subtitle {
    font-size: 0.875rem;
    color: #606266;
  }
}

.error-alert {
  margin-bottom: 1rem;
}

.login-form {
  margin-bottom: 1rem;

  :deep(.el-form-item) {
    margin-bottom: 1rem;
  }

  .submit-btn {
    width: 100%;
    background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
    border: none;

    &:hover {
      box-shadow: 0 4px 12px rgba(107, 92, 231, 0.35);
    }
  }
}

.role-select {
  text-align: center;
  margin-bottom: 1rem;

  .role-label {
    font-size: 0.75rem;
    color: #606266;
    margin-bottom: 0.75rem;
  }

  .role-options {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
  }

  .role-option {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    border-radius: 50%;
    cursor: pointer;
    transition: all 0.3s;
    color: #606266;

    &:hover {
      background: #f5f7fa;
    }

    &.active {
      background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
      color: #6B5CE7;
      border: 2px solid #6B5CE7;
    }

    span {
      font-size: 0.75rem;
      margin-top: 0.25rem;
    }
  }
}

.switch-mode {
  text-align: center;
}
</style>

<template>
  <div class="user-center-page">
    <h1 class="page-title">个人中心</h1>
    
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="menu-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">个人中心</span>
            </div>
          </template>
          
          <el-menu
            :default-active="activeMenu"
            mode="vertical"
            @select="handleMenuSelect"
          >
            <el-menu-item index="info">
              <el-icon><User /></el-icon>
              <span>个人信息</span>
            </el-menu-item>
            <el-menu-item index="security">
              <el-icon><Lock /></el-icon>
              <span>账号安全</span>
            </el-menu-item>
            <el-menu-item index="history">
              <el-icon><Clock /></el-icon>
              <span>历史记录</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>
      
      <el-col :span="18">
        <el-card v-if="activeMenu === 'info'">
          <template #header>
            <div class="card-header">
              <span class="card-title">个人信息</span>
            </div>
          </template>
          
          <div class="info-content">
            <el-form :model="formData" :rules="rules" ref="formRef" label-width="120px">
              <el-form-item label="头像">
                <div class="avatar-upload">
                  <el-avatar :size="100" :src="formData.avatar_url || defaultAvatar">
                    <template #default>
                      <el-icon><User /></el-icon>
                    </template>
                  </el-avatar>
                  <el-button type="primary" size="small" @click="handleAvatarUpload">
                    上传头像
                  </el-button>
                </div>
              </el-form-item>
              
              <el-form-item label="用户名">
                <el-input v-model="formData.username" disabled />
              </el-form-item>
              
              <el-form-item label="昵称">
                <el-input v-model="formData.nickname" placeholder="请输入昵称" />
              </el-form-item>
              
              <el-form-item label="手机号">
                <el-input v-model="formData.phone" placeholder="请输入手机号" />
              </el-form-item>
              
              <el-form-item label="个人简介">
                <el-input 
                  v-model="formData.bio" 
                  type="textarea" 
                  :rows="4" 
                  placeholder="请输入个人简介"
                />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handleSubmit" :loading="loading">
                  保存修改
                </el-button>
                <el-button @click="handleReset">
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
        
        <el-card v-if="activeMenu === 'security'">
          <template #header>
            <div class="card-header">
              <span class="card-title">账号安全</span>
            </div>
          </template>
          
          <div class="security-content">
            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="120px">
              <el-form-item label="原密码">
                <el-input 
                  v-model="passwordForm.old_password" 
                  type="password" 
                  placeholder="请输入原密码"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="新密码">
                <el-input 
                  v-model="passwordForm.new_password" 
                  type="password" 
                  placeholder="请输入新密码（至少6位）"
                  show-password
                />
              </el-form-item>
              
              <el-form-item label="确认密码">
                <el-input 
                  v-model="passwordForm.confirm_password" 
                  type="password" 
                  placeholder="请再次输入新密码"
                  show-password
                />
              </el-form-item>
              
              <el-form-item>
                <el-button type="primary" @click="handlePasswordSubmit" :loading="passwordLoading">
                  修改密码
                </el-button>
                <el-button @click="handlePasswordReset">
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>
        
        <el-card v-if="activeMenu === 'history'">
          <template #header>
            <div class="card-header">
              <span class="card-title">历史记录</span>
              <el-button type="primary" size="small" @click="handleRefresh" :loading="historyLoading">
                刷新
              </el-button>
            </div>
          </template>
          
          <div v-if="historyLoading" class="loading-container">
            <el-skeleton :rows="5" animated />
          </div>
          
          <div v-else-if="histories.length === 0" class="empty-container">
            <el-empty description="暂无历史记录" />
          </div>
          
          <el-timeline v-else>
            <el-timeline-item
              v-for="item in histories"
              :key="item.id"
              :timestamp="formatDate(item.created_at)"
              placement="top"
            >
              <el-card>
                <div class="history-item">
                  <div class="history-header">
                    <el-tag :type="getActionTypeColor(item.action_type)" size="small">
                      {{ getActionTypeLabel(item.action_type) }}
                    </el-tag>
                    <span class="history-time">{{ formatTime(item.created_at) }}</span>
                  </div>
                  <div class="history-description">
                    {{ item.description || '无描述' }}
                  </div>
                </div>
              </el-card>
            </el-timeline-item>
          </el-timeline>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock, Clock } from '@element-plus/icons-vue'

const activeMenu = ref('info')

const defaultAvatar = 'https://cube.elemecdn.com/0/88dd03763e4e4c1a925c39e0b8fdcbc3.jpeg'

const formData = ref({
  username: '',
  nickname: '',
  phone: '',
  avatar_url: '',
  bio: ''
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const formRef = ref()
const passwordFormRef = ref()
const loading = ref(false)
const passwordLoading = ref(false)
const historyLoading = ref(false)
const histories = ref<any[]>([])

const rules = {
  nickname: [
    { required: false, message: '请输入昵称', trigger: 'blur' },
    { min: 2, max: 20, message: '昵称长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ]
}

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== passwordForm.value.new_password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入原密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, validator: validateConfirmPassword, trigger: 'blur' }
  ]
}

const loadUserInfo = () => {
  const authStorage = localStorage.getItem('auth-storage')
  if (authStorage) {
    try {
      const authData = JSON.parse(authStorage)
      const user = authData?.user
      
      if (user) {
        formData.value = {
          username: user.username || '',
          nickname: user.nickname || '',
          phone: user.phone || '',
          avatar_url: user.avatar_url || '',
          bio: user.bio || ''
        }
      }
    } catch (e) {
      console.error('解析用户信息失败:', e)
    }
  }
}

const loadHistories = () => {
  historyLoading.value = true
  const mockHistories = [
    {
      id: 1,
      action_type: 'view_job',
      description: '查看了前端开发工程师岗位',
      created_at: new Date().toISOString()
    },
    {
      id: 2,
      action_type: 'update_profile',
      description: '更新了个人资料',
      created_at: new Date(Date.now() - 3600000).toISOString()
    },
    {
      id: 3,
      action_type: 'upload_resume',
      description: '上传了简历文件',
      created_at: new Date(Date.now() - 7200000).toISOString()
    }
  ]
  
  setTimeout(() => {
    histories.value = mockHistories
    historyLoading.value = false
  }, 500)
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        ElMessage.success('个人信息保存成功（本地存储）')
        localStorage.setItem('user_info', JSON.stringify(formData.value))
      } catch (error) {
        console.error('保存失败:', error)
        ElMessage.error('保存失败，请重试')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleReset = () => {
  loadUserInfo()
}

const handleAvatarUpload = () => {
  ElMessage.info('头像上传功能开发中...')
}

const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      passwordLoading.value = true
      try {
        ElMessage.success('密码修改成功（模拟）')
        handlePasswordReset()
      } catch (error) {
        console.error('修改失败:', error)
        ElMessage.error('修改失败，请重试')
      } finally {
        passwordLoading.value = false
      }
    }
  })
}

const handlePasswordReset = () => {
  passwordForm.value = {
    old_password: '',
    new_password: '',
    confirm_password: ''
  }
  passwordFormRef.value?.clearValidate()
}

const handleRefresh = () => {
  loadHistories()
}

const handleMenuSelect = (index: string) => {
  activeMenu.value = index
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getActionTypeLabel = (type: string) => {
  const typeMap: Record<string, string> = {
    'view_job': '浏览岗位',
    'generate_report': '生成报告',
    'update_profile': '更新画像',
    'upload_resume': '上传简历',
    'change_password': '修改密码',
    'update_info': '更新信息'
  }
  return typeMap[type] || type
}

const getActionTypeColor = (type: string) => {
  const colorMap: Record<string, any> = {
    'view_job': 'primary',
    'generate_report': 'success',
    'update_profile': 'warning',
    'upload_resume': 'info',
    'change_password': 'danger',
    'update_info': 'info'
  }
  return colorMap[type] || 'default'
}

onMounted(() => {
  loadUserInfo()
  loadHistories()
})
</script>

<style scoped lang="scss">
.user-center-page {
  padding: 2rem;
  
  .page-title {
    font-size: 1.8rem;
    font-weight: bold;
    color: #303133;
    margin-bottom: 1.5rem;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    
    .card-title {
      font-size: 1.2rem;
      font-weight: bold;
      color: #303133;
    }
  }
  
  .info-content,
  .security-content {
    padding: 1rem;
  }
  
  .loading-container,
  .empty-container {
    padding: 2rem 0;
  }
  
  .history-item {
    .history-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.5rem;
      
      .history-time {
        font-size: 0.85rem;
        color: #909399;
      }
    }
    
    .history-description {
      margin-bottom: 1rem;
      color: #606266;
      line-height: 1.6;
    }
  }
  
  :deep(.el-timeline-item__timestamp) {
    font-weight: bold;
    color: #409EFF;
  }
}
</style>
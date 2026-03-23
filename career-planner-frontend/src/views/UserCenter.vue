<template>
  <div class="user-center-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <el-icon :size="28">
            <User />
          </el-icon>
        </div>
        <div class="header-info">
          <h1 class="page-title">个人中心</h1>
          <p class="page-subtitle">管理您的个人信息和账号设置</p>
        </div>
      </div>
    </div>

    <el-row :gutter="24">
      <!-- 左侧菜单 -->
      <el-col :span="6">
        <el-card class="menu-card" shadow="hover">
          <div class="user-brief">
            <div class="avatar-wrapper" @click="openAvatarDialog">
              <el-avatar :size="80" :src="getAvatarUrl(formData.avatar_url)">
                <template #default>
                  <el-icon :size="40">
                    <User />
                  </el-icon>
                </template>
              </el-avatar>
              <div class="avatar-overlay">
                <el-icon>
                  <Camera />
                </el-icon>
              </div>
            </div>
            <div class="user-name">{{ formData.nickname || formData.username || '用户' }}</div>
            <div class="user-desc">{{ formData.bio || '暂无个人简介' }}</div>
          </div>

          <el-menu :default-active="activeMenu" mode="vertical" @select="handleMenuSelect" class="side-menu">
            <el-menu-item index="info">
              <el-icon>
                <User />
              </el-icon>
              <span>个人信息</span>
            </el-menu-item>
            <el-menu-item index="security">
              <el-icon>
                <Lock />
              </el-icon>
              <span>账号安全</span>
            </el-menu-item>
            <el-menu-item index="history">
              <el-icon>
                <Clock />
              </el-icon>
              <span>历史记录</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>

      <!-- 右侧内容 -->
      <el-col :span="18">
        <!-- 个人信息 -->
        <el-card v-if="activeMenu === 'info'" class="content-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">个人信息</span>
            </div>
          </template>

          <div class="info-content">
            <el-form :model="formData" :rules="rules" ref="formRef" label-width="100px">
              <el-form-item label="头像">
                <div class="avatar-setting">
                  <el-avatar :size="60" :src="getAvatarUrl(formData.avatar_url)">
                    <template #default>
                      <el-icon :size="30">
                        <User />
                      </el-icon>
                    </template>
                  </el-avatar>
                  <div class="avatar-actions">
                    <el-button type="primary" plain @click="openAvatarDialog">
                      <el-icon>
                        <Upload />
                      </el-icon>
                      更换头像
                    </el-button>
                    <span class="avatar-tip">支持 JPG、PNG、GIF 格式，大小不超过 5MB</span>
                  </div>
                </div>
              </el-form-item>

              <el-form-item label="用户名">
                <el-input v-model="formData.username" disabled placeholder="用户名不可修改" />
              </el-form-item>

              <el-form-item label="昵称" prop="nickname">
                <el-input v-model="formData.nickname" placeholder="请输入昵称" maxlength="20" show-word-limit />
              </el-form-item>

              <el-form-item label="手机号" prop="phone">
                <el-input v-model="formData.phone" placeholder="请输入手机号" maxlength="11" />
              </el-form-item>

              <el-form-item label="个人简介">
                <el-input v-model="formData.bio" type="textarea" :rows="4" placeholder="介绍一下自己吧..." maxlength="200"
                  show-word-limit />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="handleSubmit" :loading="loading">
                  <el-icon>
                    <Check />
                  </el-icon>
                  保存修改
                </el-button>
                <el-button @click="handleReset">
                  <el-icon>
                    <RefreshRight />
                  </el-icon>
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>

        <!-- 账号安全 -->
        <el-card v-if="activeMenu === 'security'" class="content-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">账号安全</span>
            </div>
          </template>

          <div class="security-content">
            <div class="security-item">
              <div class="security-icon">
                <el-icon :size="24">
                  <Lock />
                </el-icon>
              </div>
              <div class="security-info">
                <div class="security-title">登录密码</div>
                <div class="security-desc">定期更改密码有助于保护账号安全</div>
              </div>
            </div>

            <el-form :model="passwordForm" :rules="passwordRules" ref="passwordFormRef" label-width="100px"
              class="password-form">
              <el-form-item label="原密码" prop="old_password">
                <el-input v-model="passwordForm.old_password" type="password" placeholder="请输入原密码" show-password />
              </el-form-item>

              <el-form-item label="新密码" prop="new_password">
                <el-input v-model="passwordForm.new_password" type="password" placeholder="请输入新密码（至少6位）"
                  show-password />
              </el-form-item>

              <el-form-item label="确认密码" prop="confirm_password">
                <el-input v-model="passwordForm.confirm_password" type="password" placeholder="请再次输入新密码"
                  show-password />
              </el-form-item>

              <el-form-item>
                <el-button type="primary" @click="handlePasswordSubmit" :loading="passwordLoading">
                  <el-icon>
                    <Check />
                  </el-icon>
                  修改密码
                </el-button>
                <el-button @click="handlePasswordReset">
                  重置
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-card>

        <!-- 历史记录 -->
        <el-card v-if="activeMenu === 'history'" class="content-card" shadow="hover">
          <template #header>
            <div class="card-header">
              <span class="card-title">历史记录</span>
              <el-button type="primary" plain size="small" @click="handleRefresh" :loading="historyLoading">
                <el-icon>
                  <Refresh />
                </el-icon>
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

          <div v-else class="history-list">
            <div class="history-item" v-for="item in histories" :key="item.id">
              <div class="history-icon" :class="getActionTypeClass(item.action_type)">
                <el-icon :size="20">
                  <View v-if="item.action_type === 'view_job'" />
                  <Document v-else-if="item.action_type === 'upload_resume'" />
                  <Edit v-else-if="item.action_type === 'update_profile'" />
                  <Key v-else-if="item.action_type === 'change_password'" />
                  <Timer />
                </el-icon>
              </div>
              <div class="history-content">
                <div class="history-header">
                  <el-tag :type="getActionTypeColor(item.action_type)" size="small" effect="light">
                    {{ getActionTypeLabel(item.action_type) }}
                  </el-tag>
                  <span class="history-time">{{ formatDateTime(item.created_at) }}</span>
                </div>
                <div class="history-description">
                  {{ item.description || '无描述' }}
                </div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 头像上传对话框 -->
    <el-dialog v-model="avatarDialogVisible" title="更换头像" width="500px" :close-on-click-modal="false"
      class="avatar-dialog">
      <div class="avatar-upload-area">
        <el-upload ref="avatarUploadRef" class="avatar-uploader" drag :auto-upload="false" :show-file-list="false"
          :on-change="handleAvatarChange" accept="image/jpeg,image/png,image/gif,image/webp">
          <div v-if="previewAvatar" class="avatar-preview">
            <img :src="previewAvatar" alt="预览" />
          </div>
          <div v-else class="upload-placeholder">
            <el-icon class="upload-icon" :size="48">
              <Plus />
            </el-icon>
            <div class="upload-text">
              <p>点击或拖拽上传</p>
              <p class="upload-tip">支持 JPG、PNG、GIF、WEBP 格式</p>
            </div>
          </div>
        </el-upload>
      </div>

      <template #footer>
        <el-button @click="avatarDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleAvatarUpload" :loading="avatarUploading"
          :disabled="!selectedAvatarFile">
          <el-icon v-if="!avatarUploading">
            <Check />
          </el-icon>
          {{ avatarUploading ? '上传中...' : '确认上传' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import {
  User, Lock, Clock, Camera, Upload, Check, RefreshRight,
  Refresh, View, Document, Edit, Key, Timer, Plus
} from '@element-plus/icons-vue'
import request from '@/utils/request'

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

// 头像上传相关
const avatarDialogVisible = ref(false)
const avatarUploadRef = ref()
const previewAvatar = ref('')
const selectedAvatarFile = ref<File | null>(null)
const avatarUploading = ref(false)

const rules = {
  nickname: [
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

// 获取完整的头像URL
const getAvatarUrl = (avatarUrl: string | undefined) => {
  if (!avatarUrl) return defaultAvatar
  if (avatarUrl.startsWith('http')) return avatarUrl
  return `http://localhost:8001${avatarUrl}`
}

// 加载用户信息
const loadUserInfo = async () => {
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

  // 从后端获取最新资料
  try {
    const response = await request.get('/user-center/profile')
    if (response.data?.success && response.data?.data) {
      formData.value = {
        username: formData.value.username,
        nickname: response.data.data.nickname || '',
        phone: response.data.data.phone || '',
        avatar_url: response.data.data.avatar_url || '',
        bio: response.data.data.bio || ''
      }
    }
  } catch (error) {
    console.error('获取用户资料失败:', error)
  }
}

// 加载历史记录
const loadHistories = async () => {
  historyLoading.value = true
  try {
    const response = await request.get('/user-center/history')
    if (response.data?.success && response.data?.data) {
      histories.value = response.data.data
    }
  } catch (error) {
    console.error('获取历史记录失败:', error)
    // 使用模拟数据
    histories.value = [
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
  } finally {
    historyLoading.value = false
  }
}

// 提交个人信息
const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true
      try {
        const formDataToSend = new FormData()
        if (formData.value.nickname) {
          formDataToSend.append('nickname', formData.value.nickname)
        }
        if (formData.value.phone) {
          formDataToSend.append('phone', formData.value.phone)
        }
        if (formData.value.bio) {
          formDataToSend.append('bio', formData.value.bio)
        }

        const response = await request.post('/user-center/update-profile', formDataToSend, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        })

        if (response.data?.success) {
          ElMessage.success('个人信息保存成功')
          // 更新本地存储
          const authStorage = localStorage.getItem('auth-storage')
          if (authStorage) {
            const authData = JSON.parse(authStorage)
            authData.user = {
              ...authData.user,
              ...formData.value
            }
            localStorage.setItem('auth-storage', JSON.stringify(authData))
          }
        }
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

// 打开头像上传对话框
const openAvatarDialog = () => {
  previewAvatar.value = formData.value.avatar_url ? getAvatarUrl(formData.value.avatar_url) : ''
  selectedAvatarFile.value = null
  avatarDialogVisible.value = true
}

// 处理头像选择
const handleAvatarChange = (file: any) => {
  if (file.raw) {
    // 验证文件类型
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if (!allowedTypes.includes(file.raw.type)) {
      ElMessage.error('仅支持 JPG、PNG、GIF、WEBP 格式')
      return
    }

    // 验证文件大小 (5MB)
    if (file.raw.size > 5 * 1024 * 1024) {
      ElMessage.error('文件大小不能超过 5MB')
      return
    }

    selectedAvatarFile.value = file.raw

    // 创建预览
    const reader = new FileReader()
    reader.onload = (e) => {
      previewAvatar.value = e.target?.result as string
    }
    reader.readAsDataURL(file.raw)
  }
}

// 上传头像
const handleAvatarUpload = async () => {
  if (!selectedAvatarFile.value) {
    ElMessage.warning('请先选择头像')
    return
  }

  avatarUploading.value = true
  try {
    const formDataToSend = new FormData()
    formDataToSend.append('file', selectedAvatarFile.value)

    const response = await request.post('/user-center/upload-avatar', formDataToSend, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.data?.success && response.data?.data) {
      formData.value.avatar_url = response.data.data.avatar_url
      ElMessage.success('头像上传成功')
      avatarDialogVisible.value = false

      // 更新本地存储
      const authStorage = localStorage.getItem('auth-storage')
      if (authStorage) {
        const authData = JSON.parse(authStorage)
        authData.user = {
          ...authData.user,
          avatar_url: response.data.data.avatar_url
        }
        localStorage.setItem('auth-storage', JSON.stringify(authData))
      }
    }
  } catch (error: any) {
    console.error('上传失败:', error)
    ElMessage.error(error.response?.data?.detail || '上传失败，请重试')
  } finally {
    avatarUploading.value = false
  }
}

// 修改密码
const handlePasswordSubmit = async () => {
  if (!passwordFormRef.value) return

  await passwordFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      passwordLoading.value = true
      try {
        const response = await request.post('/user-center/change-password', {
          old_password: passwordForm.value.old_password,
          new_password: passwordForm.value.new_password,
          confirm_password: passwordForm.value.confirm_password
        })

        if (response.data?.success) {
          ElMessage.success('密码修改成功')
          handlePasswordReset()
        }
      } catch (error: any) {
        console.error('修改失败:', error)
        ElMessage.error(error.response?.data?.detail || '修改失败，请重试')
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

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
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

const getActionTypeClass = (type: string) => {
  const classMap: Record<string, string> = {
    'view_job': 'type-primary',
    'generate_report': 'type-success',
    'update_profile': 'type-warning',
    'upload_resume': 'type-info',
    'change_password': 'type-danger',
    'update_info': 'type-info'
  }
  return classMap[type] || ''
}

onMounted(() => {
  loadUserInfo()
  loadHistories()
})
</script>

<style scoped lang="scss">
.user-center-page {
  padding: 0;

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

  // 左侧菜单卡片
  .menu-card {
    border-radius: 16px;
    border: none;
    position: sticky;
    top: 1rem;

    :deep(.el-card__body) {
      padding: 0;
    }

    .user-brief {
      padding: 1.5rem;
      text-align: center;
      border-bottom: 1px solid #f0f0f0;
      background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
      border-radius: 16px 16px 0 0;

      .avatar-wrapper {
        position: relative;
        display: inline-block;
        cursor: pointer;

        &:hover .avatar-overlay {
          opacity: 1;
        }

        .avatar-overlay {
          position: absolute;
          inset: 0;
          background: rgba(0, 0, 0, 0.5);
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          color: #fff;
          opacity: 0;
          transition: opacity 0.3s;
        }
      }

      .user-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #303133;
        margin-top: 0.75rem;
      }

      .user-desc {
        font-size: 0.85rem;
        color: #909399;
        margin-top: 0.25rem;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        padding: 0 1rem;
      }
    }

    .side-menu {
      border: none;
      padding: 0.5rem;

      :deep(.el-menu-item) {
        border-radius: 8px;
        margin: 4px 0;
        height: 48px;
        line-height: 48px;

        &:hover {
          background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
        }

        &.is-active {
          background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
          color: #fff;

          .el-icon {
            color: #fff;
          }
        }

        .el-icon {
          font-size: 18px;
          color: #909399;
        }
      }
    }
  }

  // 右侧内容卡片
  .content-card {
    border-radius: 16px;
    border: none;
    min-height: 500px;

    :deep(.el-card__header) {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #f0f0f0;
    }

    :deep(.el-card__body) {
      padding: 1.5rem;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #303133;
        display: flex;
        align-items: center;
        gap: 0.5rem;

        &::before {
          content: '';
          width: 4px;
          height: 18px;
          background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
          border-radius: 2px;
        }
      }
    }
  }

  // 头像设置
  .avatar-setting {
    display: flex;
    align-items: center;
    gap: 1rem;

    .avatar-actions {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;

      .avatar-tip {
        font-size: 0.75rem;
        color: #909399;
      }
    }
  }

  // 表单样式
  :deep(.el-form-item) {
    margin-bottom: 1.5rem;

    .el-form-item__label {
      font-weight: 500;
      color: #606266;
    }

    .el-input__wrapper,
    .el-textarea__inner {
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        box-shadow: 0 0 0 1px #c0c4cc inset;
      }

      &.is-focus,
      &:focus {
        box-shadow: 0 0 0 1px #6B5CE7 inset !important;
      }
    }

    .el-input.is-disabled .el-input__wrapper {
      background: #f5f7fa;
    }
  }

  // 按钮样式
  :deep(.el-button--primary) {
    background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
    border: none;
    border-radius: 8px;

    &:hover {
      box-shadow: 0 4px 12px rgba(107, 92, 231, 0.35);
    }

    &.is-plain {
      background: rgba(107, 92, 231, 0.1);
      color: #6B5CE7;
      border: 1px solid rgba(107, 92, 231, 0.3);

      &:hover {
        background: rgba(107, 92, 231, 0.15);
      }
    }
  }

  // 账号安全
  .security-content {
    .security-item {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1rem;
      background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
      border-radius: 12px;
      margin-bottom: 1.5rem;

      .security-icon {
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
      }

      .security-info {
        .security-title {
          font-size: 1rem;
          font-weight: 600;
          color: #303133;
        }

        .security-desc {
          font-size: 0.85rem;
          color: #909399;
          margin-top: 0.25rem;
        }
      }
    }

    .password-form {
      max-width: 400px;
    }
  }

  // 历史记录
  .history-list {
    .history-item {
      display: flex;
      gap: 1rem;
      padding: 1rem;
      border-radius: 12px;
      margin-bottom: 0.75rem;
      background: #fafafa;
      transition: all 0.3s ease;

      &:hover {
        background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
        transform: translateX(4px);
      }

      .history-icon {
        width: 44px;
        height: 44px;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;

        &.type-primary {
          background: rgba(107, 92, 231, 0.1);
          color: #6B5CE7;
        }

        &.type-success {
          background: rgba(103, 194, 58, 0.1);
          color: #67C23A;
        }

        &.type-warning {
          background: rgba(230, 162, 60, 0.1);
          color: #E6A23C;
        }

        &.type-info {
          background: rgba(144, 147, 153, 0.1);
          color: #909399;
        }

        &.type-danger {
          background: rgba(245, 108, 108, 0.1);
          color: #F56C6C;
        }
      }

      .history-content {
        flex: 1;

        .history-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.5rem;

          .history-time {
            font-size: 0.8rem;
            color: #909399;
          }
        }

        .history-description {
          font-size: 0.9rem;
          color: #606266;
          line-height: 1.5;
        }
      }
    }
  }

  .loading-container,
  .empty-container {
    padding: 3rem 0;
  }
}

// 头像上传对话框
.avatar-dialog {
  :deep(.el-dialog) {
    border-radius: 16px;

    .el-dialog__header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #f0f0f0;
      margin: 0;
    }

    .el-dialog__body {
      padding: 1.5rem;
    }

    .el-dialog__footer {
      padding: 1rem 1.5rem;
      border-top: 1px solid #f0f0f0;
    }
  }
}

.avatar-upload-area {
  .avatar-uploader {
    :deep(.el-upload-dragger) {
      width: 100%;
      height: 280px;
      border: 2px dashed #e0e0e0;
      border-radius: 12px;
      background: #fafafa;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.3s ease;

      &:hover {
        border-color: #6B5CE7;
        background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
      }
    }
  }

  .avatar-preview {
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    img {
      max-width: 200px;
      max-height: 200px;
      border-radius: 50%;
      object-fit: cover;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
  }

  .upload-placeholder {
    text-align: center;

    .upload-icon {
      color: #c0c4cc;
      margin-bottom: 1rem;
    }

    .upload-text {
      p {
        margin: 0.5rem 0;
        color: #606266;
      }

      .upload-tip {
        font-size: 0.85rem;
        color: #909399;
      }
    }
  }
}
</style>

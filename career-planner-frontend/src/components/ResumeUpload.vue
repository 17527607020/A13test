<template>
  <div class="resume-upload">
    <el-upload
      ref="uploadRef"
      class="upload-dragger"
      drag
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleFileChange"
      :before-upload="beforeUpload"
      accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
    >
      <el-icon class="upload-icon" :size="67"><UploadFilled /></el-icon>
      <div class="upload-content">
        <div class="upload-text">
          <p class="upload-title">拖拽文件到此处</p>
          <p class="upload-hint">或 <em>点击上传</em></p>
        </div>
        <p class="upload-tips">支持 PDF、Word、图片格式，文件大小不超过 10MB</p>
      </div>
    </el-upload>
    
    <el-dialog v-model="previewVisible" title="简历预览" width="60%">
      <div class="preview-content">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="文件名">{{ fileName }}</el-descriptions-item>
          <el-descriptions-item label="文件大小">{{ fileSize }}</el-descriptions-item>
          <el-descriptions-item label="文件类型">{{ fileType }}</el-descriptions-item>
        </el-descriptions>
        <div class="preview-actions">
          <el-button type="primary" @click="handleUpload" :loading="uploading">
            {{ uploading ? '解析中...' : '开始解析' }}
          </el-button>
          <el-button @click="previewVisible = false">取消</el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled } from '@element-plus/icons-vue'
import { studentProfileApi } from '@/api/studentProfile'

const emit = defineEmits<{
  upload: [data: any]
}>()

const uploadRef = ref()
const previewVisible = ref(false)
const uploading = ref(false)
const fileName = ref('')
const fileSize = ref('')
const fileType = ref('')
const selectedFile = ref<File | null>(null)

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  const f = (bytes / Math.pow(k, i)).toFixed(2)
  return `${f} ${sizes[i]}`
}

const handleFileChange = (file: any) => {
  if (file.raw) {
    selectedFile.value = file.raw
    fileName.value = file.name
    fileSize.value = formatFileSize(file.size)
    fileType.value = file.raw.type
    previewVisible.value = true
  }
}

const beforeUpload = (file: File) => {
  const maxSize = 10 * 1024 * 1024
  if (file.size > maxSize) {
    ElMessage.error('文件大小不能超过 10MB')
    return false
  }
  
  const allowedTypes = [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/msword',
    'image/jpeg',
    'image/png'
  ]
  
  if (!allowedTypes.includes(file.type)) {
    ElMessage.error('不支持的文件格式')
    return false
  }
  
  return true
}

const handleUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.warning('请先选择文件')
    return
  }
  
  uploading.value = true
  
  try {
    const response = await studentProfileApi.uploadResume(selectedFile.value)
    
    if (response.success && response.data) {
      ElMessage.success('简历解析成功')
      emit('upload', response.data)
      previewVisible.value = false
      resetUpload()
    } else {
      ElMessage.error('简历解析失败')
    }
  } catch (error: any) {
    console.error('上传失败:', error)
    ElMessage.error(error.response?.data?.detail || '上传失败，请重试')
  } finally {
    uploading.value = false
  }
}

const resetUpload = () => {
  selectedFile.value = null
  fileName.value = ''
  fileSize.value = ''
  fileType.value = ''
}
</script>

<style scoped lang="scss">
.resume-upload {
  .upload-dragger {
    width: 100%;
    min-height: 300px;
    border: 2px dashed #d9d9d9;
    border-radius: 8px;
    background: #fafafa;
    transition: all 0.3s;
    
    &:hover {
      border-color: #409EFF;
      background: #f0f9ff;
    }
  }
  
  .upload-icon {
    font-size: 67px;
    color: #c0c4cc;
    margin-bottom: 16px;
  }
  
  .upload-content {
    padding: 20px;
    text-align: center;
  }
  
  .upload-title {
    font-size: 16px;
    font-weight: 500;
    color: #303133;
    margin-bottom: 8px;
  }
  
  .upload-hint {
    font-size: 14px;
    color: #606266;
    margin-bottom: 12px;
    
    em {
      color: #409EFF;
      font-style: normal;
    }
  }
  
  .upload-tips {
    font-size: 12px;
    color: #909399;
    margin-top: 8px;
  }
  
  .preview-content {
    .preview-actions {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      margin-top: 20px;
    }
  }
}
</style>

<template>
  <div class="resume-upload">
    <div class="upload-header">
      <div class="header-icon">
        <el-icon :size="24">
          <Document />
        </el-icon>
      </div>
      <div class="header-text">
        <h3 class="upload-title">简历上传</h3>
        <p class="upload-desc">上传简历，自动解析并填充表单信息</p>
      </div>
    </div>

    <el-upload ref="uploadRef" class="upload-dragger" drag :auto-upload="false" :show-file-list="false"
      :on-change="handleFileChange" :before-upload="beforeUpload" accept=".pdf,.doc,.docx,.jpg,.jpeg,.png">
      <div class="upload-content">
        <div class="upload-icon-wrapper">
          <el-icon class="upload-icon" :size="48">
            <UploadFilled />
          </el-icon>
        </div>
        <div class="upload-text">
          <p class="upload-main-text">拖拽文件到此处上传</p>
          <p class="upload-hint">或 <em>点击选择文件</em></p>
        </div>
        <div class="upload-divider"></div>
        <p class="upload-tips">支持 PDF、Word、图片格式，文件大小不超过 10MB</p>
      </div>
    </el-upload>

    <el-dialog v-model="previewVisible" title="简历预览" width="500px" :close-on-click-modal="false" class="preview-dialog">
      <div class="preview-content">
        <div class="file-info-card">
          <div class="file-icon">
            <el-icon :size="32">
              <Document />
            </el-icon>
          </div>
          <div class="file-details">
            <div class="file-name">{{ fileName }}</div>
            <div class="file-meta">
              <span class="meta-item">{{ fileSize }}</span>
              <span class="meta-divider">|</span>
              <span class="meta-item">{{ fileType }}</span>
            </div>
          </div>
        </div>

        <div class="preview-actions">
          <el-button @click="previewVisible = false">取消</el-button>
          <el-button type="primary" @click="handleUpload" :loading="uploading">
            <el-icon v-if="!uploading">
              <Check />
            </el-icon>
            {{ uploading ? '解析中...' : '开始解析' }}
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UploadFilled, Document, Check } from '@element-plus/icons-vue'
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
  .upload-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1.25rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #f0f0f0;

    .header-icon {
      width: 48px;
      height: 48px;
      background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
    }

    .header-text {
      .upload-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #303133;
        margin: 0 0 0.25rem 0;
      }

      .upload-desc {
        font-size: 0.875rem;
        color: #909399;
        margin: 0;
      }
    }
  }

  .upload-dragger {
    width: 100%;

    :deep(.el-upload-dragger) {
      width: 100%;
      min-height: 200px;
      border: 2px dashed #e0e0e0;
      border-radius: 16px;
      background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
      transition: all 0.3s ease;
      display: flex;
      align-items: center;
      justify-content: center;

      &:hover {
        border-color: #6B5CE7;
        background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);

        .upload-icon-wrapper {
          background: rgba(107, 92, 231, 0.15);
          transform: scale(1.05);
        }

        .upload-icon {
          color: #6B5CE7;
        }
      }
    }
  }

  .upload-content {
    text-align: center;
    padding: 1.5rem;

    .upload-icon-wrapper {
      width: 80px;
      height: 80px;
      background: rgba(107, 92, 231, 0.1);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      margin: 0 auto 1rem;
      transition: all 0.3s ease;
    }

    .upload-icon {
      color: #6B5CE7;
      transition: all 0.3s ease;
    }

    .upload-text {
      margin-bottom: 1rem;

      .upload-main-text {
        font-size: 1rem;
        font-weight: 500;
        color: #303133;
        margin: 0 0 0.5rem 0;
      }

      .upload-hint {
        font-size: 0.875rem;
        color: #909399;
        margin: 0;

        em {
          color: #6B5CE7;
          font-style: normal;
          font-weight: 500;
          cursor: pointer;
        }
      }
    }

    .upload-divider {
      width: 60px;
      height: 1px;
      background: #e0e0e0;
      margin: 1rem auto;
    }

    .upload-tips {
      font-size: 0.75rem;
      color: #c0c4cc;
      margin: 0;
    }
  }

  .preview-content {
    .file-info-card {
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 1.25rem;
      background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
      border-radius: 12px;
      margin-bottom: 1.5rem;

      .file-icon {
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #fff;
      }

      .file-details {
        flex: 1;

        .file-name {
          font-size: 1rem;
          font-weight: 600;
          color: #303133;
          margin-bottom: 0.25rem;
          word-break: break-all;
        }

        .file-meta {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.875rem;
          color: #909399;

          .meta-divider {
            color: #dcdfe6;
          }
        }
      }
    }

    .preview-actions {
      display: flex;
      justify-content: flex-end;
      gap: 0.75rem;

      :deep(.el-button) {
        min-width: 100px;
        border-radius: 8px;

        &.el-button--primary {
          background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
          border: none;
          box-shadow: 0 4px 12px rgba(107, 92, 231, 0.25);

          &:hover {
            box-shadow: 0 6px 16px rgba(107, 92, 231, 0.35);
          }
        }
      }
    }
  }
}

// 弹窗样式
:deep(.preview-dialog) {
  .el-dialog {
    border-radius: 16px;

    .el-dialog__header {
      padding: 1.25rem 1.5rem;
      border-bottom: 1px solid #f0f0f0;
      margin: 0;

      .el-dialog__title {
        font-weight: 600;
        color: #303133;
      }
    }

    .el-dialog__body {
      padding: 1.5rem;
    }
  }
}
</style>

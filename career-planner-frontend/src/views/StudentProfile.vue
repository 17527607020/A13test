<template>
  <div class="student-profile-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="header-icon">
          <el-icon :size="28">
            <User />
          </el-icon>
        </div>
        <div class="header-info">
          <h1 class="page-title">学生画像</h1>
          <p class="page-subtitle">完善个人信息，获得更精准的职业规划建议</p>
        </div>
      </div>
      <el-button type="primary" plain @click="handleLoadLastData" :disabled="!hasSavedData">
        <el-icon>
          <RefreshRight />
        </el-icon>
        返回上次信息
      </el-button>
    </div>

    <el-row :gutter="24">
      <!-- 简历上传区域 -->
      <el-col :span="24">
        <el-card class="upload-card" shadow="hover">
          <ResumeUpload @upload="handleResumeUpload" />
        </el-card>
      </el-col>

      <!-- 表单区域 -->
      <el-col :span="24">
        <el-card class="form-card" shadow="hover">
          <ProfileForm ref="profileFormRef" @save="handleProfileSave" :initial-data="loadedData" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 能力画像展示 -->
    <el-row :gutter="24" v-if="profileData">
      <el-col :span="24">
        <AbilityRadar :ability-scores="profileData.ability_scores" :summary="profileSummary" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { User, RefreshRight } from '@element-plus/icons-vue'
import ResumeUpload from '@/components/ResumeUpload.vue'
import ProfileForm from '@/components/ProfileForm.vue'
import AbilityRadar from '@/components/AbilityRadar.vue'
import { studentProfileApi } from '@/api/studentProfile'
import type { StudentProfileData } from '@/api/studentProfile'

const profileData = ref<StudentProfileData | null>(null)
const profileFormRef = ref()
const loadedData = ref<StudentProfileData | null>(null)
const hasSavedData = ref(false)

const STORAGE_KEY = 'student_profile_draft'

const checkSavedData = () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  hasSavedData.value = !!saved
}

onMounted(() => {
  checkSavedData()
})

const profileSummary = computed(() => {
  if (!profileData.value) return ''

  const scores = profileData.value.ability_scores
  const avgScore = (
    scores.professional_skills + scores.learning_ability + scores.communication +
    scores.stress_resistance + scores.innovation + scores.internship_ability
  ) / 5

  if (avgScore >= 80) return '综合能力优秀，具备很强的专业能力和学习能力，适合高级技术岗位'
  if (avgScore >= 60) return '综合能力良好，具备扎实的专业基础和实习经验，适合中级技术岗位'
  if (avgScore >= 40) return '综合能力中等，具备基本的专业技能，适合初级技术岗位'
  return '综合能力有待提升，建议加强专业技能学习和实践锻炼'
})

const handleResumeUpload = (data: StudentProfileData) => {
  profileData.value = data
  ElMessage.success('简历解析成功，请完善信息后保存')
}

const handleProfileSave = async (data: StudentProfileData) => {
  try {
    const response = await studentProfileApi.saveProfile(data)

    if (response.success) {
      profileData.value = {
        ...response.data,
        ability_scores: response.data.ability_scores || {
          professional_skills: 50,
          learning_ability: 50,
          communication: 50,
          stress_resistance: 50,
          innovation: 50,
          internship_ability: 50
        }
      }
      ElMessage.success('画像保存成功')
      checkSavedData()
    } else {
      ElMessage.error(response.message || '保存失败')
    }
  } catch (error: any) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  }
}

const handleLoadLastData = () => {
  try {
    const saved = localStorage.getItem(STORAGE_KEY)
    if (saved) {
      const parsed = JSON.parse(saved)
      loadedData.value = parsed
      profileFormRef.value?.loadData(parsed)
      ElMessage.success('已加载上次保存的学生信息')
    } else {
      ElMessage.warning('没有找到上次保存的信息')
    }
  } catch (error: any) {
    console.error('加载数据失败:', error)
    ElMessage.error('加载数据失败')
  }
}
</script>

<style scoped lang="scss">
.student-profile-page {
  padding: 0;

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

    :deep(.el-button) {
      background: rgba(255, 255, 255, 0.2);
      border-color: rgba(255, 255, 255, 0.3);
      color: #fff;

      &:hover {
        background: rgba(255, 255, 255, 0.3);
        border-color: rgba(255, 255, 255, 0.4);
      }

      &.is-disabled {
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(255, 255, 255, 0.15);
        color: rgba(255, 255, 255, 0.5);
      }
    }
  }

  .upload-card,
  .form-card {
    margin-bottom: 1.5rem;
    border-radius: 16px;
    border: none;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
    }

    :deep(.el-card__body) {
      padding: 1.5rem;
    }
  }
}
</style>

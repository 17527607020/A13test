<template>
  <div class="student-profile-page">
    <div class="page-header">
      <h1 class="page-title">学生画像</h1>
      <el-button 
        type="primary" 
        @click="handleLoadLastData"
        :disabled="!hasSavedData"
      >
        返回上次学生信息
      </el-button>
    </div>
    
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="upload-card">
          <ResumeUpload @upload="handleResumeUpload" />
        </el-card>
      </el-col>
      
      <el-col :span="24">
        <el-card class="form-card">
          <ProfileForm 
            ref="profileFormRef"
            @save="handleProfileSave" 
            :initial-data="loadedData"
          />
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" v-if="profileData">
      <el-col :span="24">
        <AbilityRadar :ability-scores="profileData.ability_scores" :summary="profileSummary" />
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
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
  padding: 2rem;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    
    .page-title {
      font-size: 1.8rem;
      font-weight: bold;
      color: #303133;
      margin: 0;
    }
  }
  
  .upload-card,
  .form-card {
    height: 100%;
  }
}
</style>

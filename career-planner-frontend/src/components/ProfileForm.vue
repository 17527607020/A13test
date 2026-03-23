<template>
  <div class="profile-form">
    <el-card>
      <template #header>
        <div class="form-header">
          <span class="form-title">学生画像</span>
          <el-button type="primary" @click="handleSave" :loading="saving">保存画像</el-button>
        </div>
      </template>

      <el-steps :active="currentStep" align-center>
        <el-step title="基本信息" @click="goToStep(0)" class="clickable-step" :status="getStepStatus(0)" />
        <el-step title="教育经历" @click="goToStep(1)" class="clickable-step" :status="getStepStatus(1)" />
        <el-step title="实习经历" @click="goToStep(2)" class="clickable-step" :status="getStepStatus(2)" />
        <el-step title="项目经历" @click="goToStep(3)" class="clickable-step" :status="getStepStatus(3)" />
        <el-step title="技能证书" @click="goToStep(4)" class="clickable-step" :status="getStepStatus(4)" />
        <el-step title="能力画像" @click="goToStep(5)" class="clickable-step" :status="getStepStatus(5)" />
      </el-steps>

      <div class="form-content">
        <el-form v-if="currentStep === 0" :model="formData.basic_info" label-width="120px" :rules="basicInfoRules"
          ref="basicFormRef">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="姓名" prop="name" required>
                <el-input v-model="formData.basic_info.name" placeholder="请输入姓名" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="性别" prop="gender" required>
                <el-select v-model="formData.basic_info.gender" placeholder="请选择性别" style="width: 100%">
                  <el-option label="男" value="男" />
                  <el-option label="女" value="女" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="年龄" prop="age" required>
                <el-input-number v-model="formData.basic_info.age" :min="16" :max="50" placeholder="请输入年龄"
                  style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="电话" prop="phone" required>
                <el-input v-model="formData.basic_info.phone" placeholder="请输入电话" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="邮箱" prop="email" required>
                <el-input v-model="formData.basic_info.email" type="email" placeholder="请输入邮箱" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="所在地" prop="locationArr" required>
                <el-cascader v-model="formData.basic_info.locationArr" :options="regionOptions" placeholder="请选择省/市/区"
                  style="width: 100%" @change="handleLocationChange" />
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>

        <div v-if="currentStep === 1" class="education-list">
          <div class="list-header">
            <span>教育经历</span>
            <el-button type="primary" size="small" @click="addEducation">添加</el-button>
          </div>
          <el-card v-for="(edu, index) in formData.education" :key="index" class="item-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>教育 #{{ index + 1 }}</span>
                <el-button type="danger" size="small" text @click="removeEducation(index)">删除</el-button>
              </div>
            </template>
            <el-form :model="edu" label-width="100px">
              <el-form-item label="学校" required>
                <el-input v-model="edu.school" placeholder="请输入学校名称" />
              </el-form-item>
              <el-form-item label="专业" required>
                <el-input v-model="edu.major" placeholder="请输入专业" />
              </el-form-item>
              <el-form-item label="学位" required>
                <el-select v-model="edu.degree" placeholder="请选择学位">
                  <el-option label="本科" value="本科" />
                  <el-option label="硕士" value="硕士" />
                  <el-option label="博士" value="博士" />
                  <el-option label="大专" value="大专" />
                </el-select>
              </el-form-item>
              <el-form-item label="开始时间">
                <el-date-picker v-model="edu.start_date" type="date" placeholder="选择开始时间" />
              </el-form-item>
              <el-form-item label="结束时间">
                <el-date-picker v-model="edu.end_date" type="date" placeholder="选择结束时间" />
              </el-form-item>
              <el-form-item label="GPA">
                <el-input v-model="edu.gpa" placeholder="请输入GPA" />
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="edu.description" type="textarea" :rows="3" placeholder="请输入描述" />
              </el-form-item>
            </el-form>
          </el-card>
        </div>

        <div v-if="currentStep === 2" class="experience-list">
          <div class="list-header">
            <span>实习经历</span>
            <el-button type="primary" size="small" @click="addExperience">添加</el-button>
          </div>
          <el-card v-for="(exp, index) in formData.experience" :key="index" class="item-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>实习 #{{ index + 1 }}</span>
                <el-button type="danger" size="small" text @click="removeExperience(index)">删除</el-button>
              </div>
            </template>
            <el-form :model="exp" label-width="100px">
              <el-form-item label="公司" required>
                <el-input v-model="exp.company" placeholder="请输入公司名称" />
              </el-form-item>
              <el-form-item label="职位" required>
                <el-input v-model="exp.position" placeholder="请输入职位" />
              </el-form-item>
              <el-form-item label="开始时间">
                <el-date-picker v-model="exp.start_date" type="date" placeholder="选择开始时间" />
              </el-form-item>
              <el-form-item label="结束时间">
                <el-date-picker v-model="exp.end_date" type="date" placeholder="选择结束时间" />
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="exp.description" type="textarea" :rows="3" placeholder="请输入工作描述" />
              </el-form-item>
            </el-form>
          </el-card>
        </div>

        <div v-if="currentStep === 3" class="project-list">
          <div class="list-header">
            <span>项目经历</span>
            <el-button type="primary" size="small" @click="addProject">添加</el-button>
          </div>
          <el-card v-for="(proj, index) in formData.projects" :key="index" class="item-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>项目 #{{ index + 1 }}</span>
                <el-button type="danger" size="small" text @click="removeProject(index)">删除</el-button>
              </div>
            </template>
            <el-form :model="proj" label-width="100px">
              <el-form-item label="项目名称" required>
                <el-input v-model="proj.name" placeholder="请输入项目名称" />
              </el-form-item>
              <el-form-item label="角色">
                <el-input v-model="proj.role" placeholder="请输入角色" />
              </el-form-item>
              <el-form-item label="开始时间">
                <el-date-picker v-model="proj.start_date" type="date" placeholder="选择开始时间" />
              </el-form-item>
              <el-form-item label="结束时间">
                <el-date-picker v-model="proj.end_date" type="date" placeholder="选择结束时间" />
              </el-form-item>
              <el-form-item label="技术栈">
                <el-select v-model="proj.technologies" multiple filterable allow-create placeholder="请选择技术栈">
                  <el-option v-for="tech in commonTechs" :key="tech" :label="tech" :value="tech" />
                </el-select>
              </el-form-item>
              <el-form-item label="描述">
                <el-input v-model="proj.description" type="textarea" :rows="3" placeholder="请输入项目描述" />
              </el-form-item>
            </el-form>
          </el-card>
        </div>

        <div v-if="currentStep === 4" class="skills-certificates">
          <div class="section">
            <div class="list-header">
              <span>技能</span>
              <el-button type="primary" size="small" @click="addSkill">添加</el-button>
            </div>
            <el-card v-for="(skill, index) in formData.skills" :key="index" class="item-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>技能 #{{ index + 1 }}</span>
                  <el-button type="danger" size="small" text @click="removeSkill(index)">删除</el-button>
                </div>
              </template>
              <el-form :model="skill" label-width="100px">
                <el-form-item label="技能名称" required>
                  <el-input v-model="skill.name" placeholder="请输入技能名称" />
                </el-form-item>
                <el-form-item label="熟练度">
                  <el-select v-model="skill.level" placeholder="请选择熟练度">
                    <el-option label="入门" value="入门" />
                    <el-option label="熟练" value="熟练" />
                    <el-option label="精通" value="精通" />
                  </el-select>
                </el-form-item>
                <el-form-item label="类别">
                  <el-input v-model="skill.category" placeholder="请输入技能类别" />
                </el-form-item>
              </el-form>
            </el-card>
          </div>

          <div class="section">
            <div class="list-header">
              <span>证书</span>
              <el-button type="primary" size="small" @click="addCertificate">添加</el-button>
            </div>
            <el-card v-for="(cert, index) in formData.certificates" :key="index" class="item-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>证书 #{{ index + 1 }}</span>
                  <el-button type="danger" size="small" text @click="removeCertificate(index)">删除</el-button>
                </div>
              </template>
              <el-form :model="cert" label-width="100px">
                <el-form-item label="证书名称" required>
                  <el-input v-model="cert.name" placeholder="请输入证书名称" />
                </el-form-item>
                <el-form-item label="颁发机构">
                  <el-input v-model="cert.issuer" placeholder="请输入颁发机构" />
                </el-form-item>
                <el-form-item label="颁发时间">
                  <el-date-picker v-model="cert.issue_date" type="date" placeholder="选择颁发时间" />
                </el-form-item>
                <el-form-item label="过期时间">
                  <el-date-picker v-model="cert.expiry_date" type="date" placeholder="选择过期时间" />
                </el-form-item>
              </el-form>
            </el-card>
          </div>

          <div class="section">
            <div class="list-header">
              <span>获奖情况</span>
              <el-button type="primary" size="small" @click="addAward">添加</el-button>
            </div>
            <el-card v-for="(award, index) in formData.awards" :key="index" class="item-card" shadow="hover">
              <template #header>
                <div class="card-header">
                  <span>奖项 #{{ index + 1 }}</span>
                  <el-button type="danger" size="small" text @click="removeAward(index)">删除</el-button>
                </div>
              </template>
              <el-form :model="award" label-width="100px">
                <el-form-item label="奖项名称" required>
                  <el-input v-model="award.name" placeholder="请输入奖项名称" />
                </el-form-item>
                <el-form-item label="级别">
                  <el-select v-model="award.level" placeholder="请选择级别">
                    <el-option label="国家级" value="国家级" />
                    <el-option label="省级" value="省级" />
                    <el-option label="市级" value="市级" />
                    <el-option label="校级" value="校级" />
                  </el-select>
                </el-form-item>
                <el-form-item label="获得时间">
                  <el-date-picker v-model="award.date" type="date" placeholder="选择获得时间" />
                </el-form-item>
                <el-form-item label="描述">
                  <el-input v-model="award.description" type="textarea" :rows="3" placeholder="请输入描述" />
                </el-form-item>
              </el-form>
            </el-card>
          </div>

          <div v-if="currentStep === 5" class="ability-profile">
            <AbilityRadar :ability-scores="formData.ability_scores" />
          </div>
        </div>
      </div>

      <div class="form-actions">
        <el-button @click="prevStep" :disabled="currentStep === 0">上一步</el-button>
        <el-button type="primary" @click="nextStep" :disabled="currentStep === 5">下一步</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import type { StudentProfileData, EducationItem, ExperienceItem, ProjectItem, SkillItem, CertificateItem, AwardItem } from '@/api/studentProfile'
import AbilityRadar from '@/components/AbilityRadar.vue'
import { chinaRegions } from '@/utils/chinaRegions'

interface Props {
  initialData?: StudentProfileData | null
}

const props = withDefaults(defineProps<Props>(), {
  initialData: null
})

const emit = defineEmits<{
  save: [data: StudentProfileData]
}>()

const currentStep = ref<number>(0)
const saving = ref(false)
const basicFormRef = ref<FormInstance>()

const STORAGE_KEY = 'student_profile_draft'

// 电话号码验证
const validatePhone = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入电话号码'))
  } else if (!/^1[3-9]\d{9}$/.test(value)) {
    callback(new Error('请输入正确的手机号码格式'))
  } else {
    callback()
  }
}

// 邮箱验证
const validateEmail = (rule: any, value: any, callback: any) => {
  if (!value) {
    callback(new Error('请输入邮箱'))
  } else if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(value)) {
    callback(new Error('请输入正确的邮箱格式'))
  } else {
    callback()
  }
}

// 基本信息验证规则
const basicInfoRules: FormRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  age: [{ required: true, message: '请输入年龄', trigger: 'blur' }],
  phone: [{ required: true, validator: validatePhone, trigger: 'blur' }],
  email: [{ required: true, validator: validateEmail, trigger: 'blur' }],
  locationArr: [{ required: true, message: '请选择所在地', trigger: 'change' }]
}

// 地区选项
const regionOptions = chinaRegions

// 处理地区选择变化
const handleLocationChange = (value: string[]) => {
  if (value && value.length > 0) {
    formData.value.basic_info.location = value.join('')
  }
}

const defaultFormData: StudentProfileData = {
  basic_info: {
    name: '',
    gender: '',
    age: undefined,
    phone: '',
    email: '',
    location: '',
    locationArr: []
  },
  education: [
    {
      school: '',
      major: '',
      degree: '',
      start_date: undefined,
      end_date: undefined,
      gpa: undefined,
      description: ''
    }
  ],
  experience: [
    {
      company: '',
      position: '',
      start_date: undefined,
      end_date: undefined,
      description: ''
    }
  ],
  projects: [
    {
      name: '',
      role: undefined,
      start_date: undefined,
      end_date: undefined,
      description: '',
      technologies: []
    }
  ],
  skills: [
    {
      name: '',
      level: undefined,
      category: undefined
    }
  ],
  certificates: [
    {
      name: '',
      issuer: undefined,
      issue_date: undefined,
      expiry_date: undefined
    }
  ],
  awards: [
    {
      name: '',
      level: undefined,
      date: undefined,
      description: ''
    }
  ],
  ability_scores: {
    professional_skills: 50,
    learning_ability: 50,
    communication: 50,
    stress_resistance: 50,
    innovation: 50,
    internship_ability: 50
  }
}

const formData = ref<StudentProfileData>({ ...defaultFormData })

const loadFromStorage = () => {
  const saved = localStorage.getItem(STORAGE_KEY)
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      return parsed
    } catch (e) {
      return null
    }
  }
  return null
}

const saveToStorage = () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(formData.value))
}

const clearStorage = () => {
  localStorage.removeItem(STORAGE_KEY)
}

const loadData = (data: StudentProfileData) => {
  formData.value = JSON.parse(JSON.stringify(data))
}

watch(() => props.initialData, (newData) => {
  if (newData) {
    loadData(newData)
  }
}, { immediate: true })

defineExpose({
  loadData
})

const commonTechs = [
  'JavaScript', 'TypeScript', 'Vue', 'React', 'Python', 'Java', 'Go', 'Node.js',
  'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Docker', 'Kubernetes',
  'Git', 'Linux', 'Nginx', 'FastAPI', 'Spring Boot'
]

const addEducation = () => {
  formData.value.education.push({
    school: '',
    major: '',
    degree: '',
    start_date: undefined,
    end_date: undefined,
    gpa: undefined,
    description: ''
  })
}

const removeEducation = (index: number) => {
  formData.value.education.splice(index, 1)
}

const addExperience = () => {
  formData.value.experience.push({
    company: '',
    position: '',
    start_date: undefined,
    end_date: undefined,
    description: ''
  })
}

const removeExperience = (index: number) => {
  formData.value.experience.splice(index, 1)
}

const addProject = () => {
  formData.value.projects.push({
    name: '',
    role: undefined,
    start_date: undefined,
    end_date: undefined,
    description: '',
    technologies: []
  })
}

const removeProject = (index: number) => {
  formData.value.projects.splice(index, 1)
}

const addSkill = () => {
  formData.value.skills.push({
    name: '',
    level: undefined,
    category: undefined
  })
}

const removeSkill = (index: number) => {
  formData.value.skills.splice(index, 1)
}

const addCertificate = () => {
  formData.value.certificates.push({
    name: '',
    issuer: undefined,
    issue_date: undefined,
    expiry_date: undefined
  })
}

const removeCertificate = (index: number) => {
  formData.value.certificates.splice(index, 1)
}

const addAward = () => {
  formData.value.awards.push({
    name: '',
    level: undefined,
    date: undefined,
    description: ''
  })
}

const removeAward = (index: number) => {
  formData.value.awards.splice(index, 1)
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}

const nextStep = () => {
  if (currentStep.value < 5) {
    currentStep.value++
  }
}

const goToStep = (step: number) => {
  currentStep.value = step
}

const validateStep = (step: number): boolean => {
  switch (step) {
    case 0:
      return !!formData.value.basic_info.name &&
        !!formData.value.basic_info.gender &&
        !!formData.value.basic_info.age &&
        !!formData.value.basic_info.phone &&
        !!formData.value.basic_info.email &&
        (formData.value.basic_info.locationArr?.length ?? 0) > 0
    case 1:
      return formData.value.education.some(edu => !!edu.school && !!edu.major && !!edu.degree)
    case 2:
      return formData.value.experience.some(exp => !!exp.company && !!exp.position)
    case 3:
      return formData.value.projects.some(proj => !!proj.name)
    case 4:
      return formData.value.skills.some(skill => !!skill.name) ||
        formData.value.certificates.some(cert => !!cert.name) ||
        formData.value.awards.some(award => !!award.name)
    case 5:
      return formData.value.ability_scores &&
        (formData.value.ability_scores.professional_skills > 0 ||
          formData.value.ability_scores.learning_ability > 0)
    default:
      return false
  }
}

const getStepStatus = (step: number): 'success' | 'process' | 'wait' => {
  if (validateStep(step)) {
    return 'success'
  }
  if (step === currentStep.value) {
    return 'process'
  }
  return 'wait'
}

const handleSave = async () => {
  // 验证基本信息
  if (currentStep.value === 0 && basicFormRef.value) {
    try {
      await basicFormRef.value.validate()
    } catch {
      ElMessage.warning('请完整填写基本信息')
      return
    }
  }

  saving.value = true
  try {
    emit('save', formData.value)
    saveToStorage()
    ElMessage.success('画像保存成功')
  } catch (error: any) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败，请重试')
  } finally {
    saving.value = false
  }
}

watch(formData, () => {
  saveToStorage()
}, { deep: true })
</script>

<style scoped lang="scss">
.profile-form {
  :deep(.el-card) {
    border: none;
    border-radius: 16px;
    box-shadow: none;
  }

  :deep(.el-card__header) {
    border-bottom: 1px solid #f0f0f0;
    padding: 1.25rem 1.5rem;
  }

  :deep(.el-card__body) {
    padding: 1.5rem;
  }

  .form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .form-title {
      font-size: 1.25rem;
      font-weight: 600;
      color: #303133;
      display: flex;
      align-items: center;
      gap: 0.5rem;

      &::before {
        content: '';
        width: 4px;
        height: 20px;
        background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
        border-radius: 2px;
      }
    }
  }

  // 步骤条美化
  :deep(.el-steps) {
    padding: 0.5rem 0;

    .el-step {
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        .el-step__title {
          color: #6B5CE7;
        }

        .el-step__icon {
          border-color: #6B5CE7;
          color: #6B5CE7;
        }
      }

      .el-step__icon {
        border-width: 2px;
        transition: all 0.3s ease;
      }

      .el-step__icon.is-text {
        background: #f5f7fa;
        border-color: #e4e7ed;
        color: #909399;
      }

      .el-step__icon.is-finish {
        background: linear-gradient(135deg, #6B5CE7 0%, #8A7FE0 100%);
        border-color: transparent;
        color: #fff;
      }

      .el-step__icon.is-process {
        background: #fff;
        border-color: #6B5CE7;
        color: #6B5CE7;
        box-shadow: 0 0 0 4px rgba(107, 92, 231, 0.1);
      }

      .el-step__title {
        font-size: 0.875rem;
        font-weight: 500;
        transition: all 0.3s ease;

        &.is-finish {
          color: #6B5CE7;
        }

        &.is-process {
          color: #303133;
          font-weight: 600;
        }
      }

      .el-step__line {
        background: #e4e7ed;
        height: 2px;

        .el-step__line-inner {
          background: linear-gradient(90deg, #6B5CE7 0%, #8A7FE0 100%);
        }
      }
    }
  }

  .form-content {
    margin-top: 2rem;
    min-height: 450px;
  }

  // 列表头部
  .list-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
    background: linear-gradient(135deg, #f8f7ff 0%, #f0ebfa 100%);
    border-radius: 10px;
    font-size: 1rem;
    font-weight: 600;
    color: #303133;
    border-left: 3px solid #6B5CE7;
  }

  // 卡片项
  .item-card {
    margin-bottom: 1rem;
    border-radius: 12px;
    border: 1px solid #ebeef5;
    transition: all 0.3s ease;

    &:hover {
      border-color: #e0e0e0;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    :deep(.el-card__header) {
      background: #fafafa;
      border-bottom: 1px solid #ebeef5;
      padding: 0.75rem 1rem;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 500;
      color: #606266;

      span {
        display: flex;
        align-items: center;
        gap: 0.5rem;

        &::before {
          content: '';
          width: 8px;
          height: 8px;
          background: #6B5CE7;
          border-radius: 50%;
        }
      }
    }
  }

  // 技能证书区域
  .skills-certificates {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1.5rem;

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }

  // 表单操作按钮
  .form-actions {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
    padding-top: 1.5rem;
    border-top: 1px solid #f0f0f0;

    :deep(.el-button) {
      min-width: 120px;
      border-radius: 8px;
      font-weight: 500;

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

  // 表单项美化
  :deep(.el-form-item) {
    margin-bottom: 1.25rem;

    .el-form-item__label {
      font-weight: 500;
      color: #606266;
    }

    .el-input__wrapper,
    .el-select__wrapper,
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

    .el-input-number {
      width: 100%;
    }

    .el-cascader {
      width: 100%;
    }
  }

  // 添加按钮
  :deep(.el-button--primary.is-text) {
    color: #6B5CE7;

    &:hover {
      color: #8A7FE0;
    }
  }

  :deep(.el-button--danger.is-text) {
    color: #F56C6C;

    &:hover {
      color: #f78989;
    }
  }
}
</style>

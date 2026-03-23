import request from '@/utils/request'

export interface BasicInfo {
  name: string
  gender?: string
  age?: number
  phone?: string
  email: string
  location?: string
  locationArr?: string[]
}

export interface EducationItem {
  school: string
  major: string
  degree: string
  start_date?: string
  end_date?: string
  gpa?: string
  description?: string
}

export interface ExperienceItem {
  company: string
  position: string
  start_date?: string
  end_date?: string
  description?: string
}

export interface ProjectItem {
  name: string
  role?: string
  start_date?: string
  end_date?: string
  description?: string
  technologies?: string[]
}

export interface SkillItem {
  name: string
  level?: string
  category?: string
}

export interface CertificateItem {
  name: string
  issuer?: string
  issue_date?: string
  expiry_date?: string
}

export interface AwardItem {
  name: string
  level?: string
  date?: string
  description?: string
}

export interface AbilityScores {
  professional_skills: number
  learning_ability: number
  communication: number
  stress_resistance: number
  innovation: number
  internship_ability: number
}

export interface StudentProfileData {
  basic_info: BasicInfo
  education: EducationItem[]
  experience: ExperienceItem[]
  projects: ProjectItem[]
  skills: SkillItem[]
  certificates: CertificateItem[]
  awards: AwardItem[]
  ability_scores: AbilityScores
}

export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}

export const studentProfileApi = {
  uploadResume(file: File): Promise<ApiResponse<StudentProfileData>> {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/students/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  parseResume(text: string): Promise<ApiResponse<StudentProfileData>> {
    const formData = new FormData()
    formData.append('text', text)
    return request.post('/students/resume/parse', formData)
  },

  getProfile(userId?: number): Promise<ApiResponse<StudentProfileData | null>> {
    const params: Record<string, number> = {}
    if (userId) params.user_id = userId
    return request.get('/students/profile', { params })
  },

  saveProfile(data: StudentProfileData, userId?: number): Promise<ApiResponse<StudentProfileData>> {
    return request.post('/students/profile', data)
  }
}

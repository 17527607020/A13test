import request from '@/utils/request'

// ============ 类型定义 ============

export interface ProgressItem {
  title: string
  value: number
  description: string
}

export interface LearningResource {
  id: number
  title: string
  description: string
  logo: string
  color: string
  tag: string
  tag_type: string
  content: string | null
  link: string | null
}

export interface AIRecommendation {
  title: string
  subtitle: string
  content: string
  avatar_icon: string
}

export interface QuickAction {
  label: string
  icon: string
  route: string
  button_type: string
}

export interface HomeData {
  username: string
  greeting: string
  progress_items: ProgressItem[]
  ai_recommendation: AIRecommendation
  learning_resources: LearningResource[]
  quick_actions: QuickAction[]
  total_assessments: number
  total_interviews: number
  total_plans: number
}

// ============ API 方法 ============

/**
 * 获取首页所有数据
 */
export function getHomeData(userId: number) {
  return request.get<any, HomeData>(`/home/data?user_id=${userId}`)
}

/**
 * 获取学习资源列表
 */
export function getLearningResources() {
  return request.get<any, LearningResource[]>('/home/resources')
}

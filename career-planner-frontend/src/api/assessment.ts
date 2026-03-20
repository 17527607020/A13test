import request from '@/utils/request'

// 测评类型接口
export interface Assessment {
  id: number
  code: string
  name: string
  description: string
  icon: string
  color: string
  duration: number
  question_count: number
  created_at: string
}

export interface QuestionOption {
  text: string
  value: string
  score: number
}

export interface AssessmentQuestion {
  id: number
  question_text: string
  question_order: number
  dimension: string | null
  options: QuestionOption[]
}

export interface AssessmentDetail extends Assessment {
  questions: AssessmentQuestion[]
}

export interface DimensionScore {
  dimension: string
  score: number
  max_score: number
  percentage: number
}

export interface AssessmentReport {
  id: number
  user_id: number
  assessment_id: number
  result_type: string
  result_name: string
  scores: Record<string, any>
  dimensions: DimensionScore[] | null
  suggestions: string | null
  total_score: number
  completed_at: string
  created_at: string
  assessment?: Assessment
}

export interface ReportListItem {
  id: number
  assessment_id: number
  assessment_name: string
  assessment_type: string
  result_type: string
  result_name: string
  completed_at: string
  color: string | null
}

export interface AnswerSubmit {
  question_id: number
  answer: string
}

export interface AssessmentSubmit {
  assessment_id: number
  answers: AnswerSubmit[]
}

// API方法

/**
 * 获取所有测评类型
 */
export function getAssessments() {
  return request.get<any, Assessment[]>('/assessment/list')
}

/**
 * 获取测评详情（包含题目）
 */
export function getAssessmentDetail(assessmentId: number) {
  return request.get<any, AssessmentDetail>(`/assessment/${assessmentId}`)
}

/**
 * 提交测评答案
 */
export function submitAssessment(data: AssessmentSubmit, userId: number) {
  return request.post<any, AssessmentReport>(`/assessment/submit?user_id=${userId}`, data)
}

/**
 * 获取我的测评报告列表
 */
export function getMyReports(userId: number) {
  return request.get<any, ReportListItem[]>(`/assessment/reports/my?user_id=${userId}`)
}

/**
 * 获取报告详情
 */
export function getReportDetail(reportId: number, userId: number) {
  return request.get<any, AssessmentReport>(`/assessment/report/${reportId}?user_id=${userId}`)
}

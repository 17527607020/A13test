import request from '@/utils/request'

// ============ 类型定义 ============

export interface InterviewMode {
  id: string
  title: string
  description: string
  icon: string
  color: string
  tags: string[]
}

export interface InterviewModesResponse {
  modes: InterviewMode[]
}

export interface JobPosition {
  id: number
  name: string
  code: string
  logo: string | null
  question_count: number
  description: string | null
  is_hot: boolean
}

export interface InterviewQuestion {
  id: number
  category: string
  job_type: string | null
  question_text: string
  difficulty: string
  tags: string[] | null
  question_order: number
}

export interface StartInterviewRequest {
  interview_mode: string
  target_job?: string
  question_count: number
}

export interface InterviewSessionCreate {
  session_id: number
  questions: InterviewQuestion[]
  total_questions: number
  started_at: string
}

export interface ScoreDetails {
  relevance: number
  depth: number
  clarity: number
  completeness: number
}

export interface AnswerFeedback {
  id: number
  question_id: number
  question_text: string
  user_answer: string
  reference_answer: string | null
  score: number
  score_details: ScoreDetails | null
  feedback: string
  suggestions: string | null
  answer_duration: number
}

export interface SubmitAnswerRequest {
  session_id: number
  question_id: number
  user_answer: string
  answer_duration: number
}

export interface InterviewSession {
  id: number
  user_id: number
  interview_mode: string
  target_job: string | null
  status: string
  total_score: number
  overall_feedback: string | null
  strengths: string[] | null
  improvements: string[] | null
  duration: number
  started_at: string | null
  completed_at: string | null
  created_at: string
}

export interface InterviewSessionDetail extends InterviewSession {
  answers: AnswerFeedback[]
}

export interface InterviewRecordItem {
  id: number
  interview_mode: string
  mode_name: string
  target_job: string | null
  status: string
  total_score: number
  question_count: number
  completed_at: string | null
  created_at: string
}

// ============ API 方法 ============

/**
 * 获取面试模式列表
 */
export function getInterviewModes() {
  return request.get<any, InterviewModesResponse>('/interview/modes')
}

/**
 * 获取岗位列表
 */
export function getJobPositions(hotOnly: boolean = false) {
  return request.get<any, JobPosition[]>('/interview/jobs', {
    params: { hot_only: hotOnly }
  })
}

/**
 * 开始面试
 */
export function startInterview(data: StartInterviewRequest, userId: number) {
  return request.post<any, InterviewSessionCreate>(
    `/interview/start?user_id=${userId}`,
    data
  )
}

/**
 * 提交回答
 */
export function submitAnswer(data: SubmitAnswerRequest, userId: number) {
  return request.post<any, AnswerFeedback>(
    `/interview/answer?user_id=${userId}`,
    data
  )
}

/**
 * 完成面试
 */
export function completeInterview(sessionId: number, userId: number) {
  return request.post<any, InterviewSession>(
    `/interview/${sessionId}/complete?user_id=${userId}`
  )
}

/**
 * 获取面试记录列表
 */
export function getInterviewRecords(userId: number, limit: number = 10) {
  return request.get<any, InterviewRecordItem[]>(
    `/interview/records?user_id=${userId}&limit=${limit}`
  )
}

/**
 * 获取面试会话详情
 */
export function getSessionDetail(sessionId: number, userId: number) {
  return request.get<any, InterviewSessionDetail>(
    `/interview/session/${sessionId}?user_id=${userId}`
  )
}

/**
 * 初始化默认数据
 */
export function initDefaultData() {
  return request.post<any, { success: boolean; message: string }>(
    '/interview/init-data'
  )
}

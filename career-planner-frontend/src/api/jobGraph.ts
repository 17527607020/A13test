import request from '@/utils/request'

export interface JobNode {
  id: string
  name: string
  type: string
  description?: string
  salary?: string
}

export interface JobLink {
  source: string
  target: string
  type: string
}

export interface JobGraphData {
  nodes: JobNode[]
  links: JobLink[]
}

export interface JobInfo {
  name: string
  type: string
  description?: string
  salary?: string
  source?: string
  promotion_count?: number
  transfer_count?: number
}

export type GraphType = 'all' | 'promotion' | 'transfer'

export const jobGraphApi = {
  getAllJobs(): Promise<JobInfo[]> {
    return request.get('/job-graph/jobs')
  },

  getJobsWithPaths(): Promise<JobInfo[]> {
    return request.get('/job-graph/jobs-with-paths')
  },

  getPromotionPaths(jobName: string): Promise<JobGraphData> {
    return request.get('/job-graph/promotion-paths', {
      params: { job_name: jobName }
    })
  },

  getTransferPaths(jobName: string): Promise<JobGraphData> {
    return request.get('/job-graph/transfer-paths', {
      params: { job_name: jobName }
    })
  },

  getFullGraph(jobName?: string, graphType?: GraphType): Promise<JobGraphData> {
    const params: Record<string, string> = {}
    if (jobName) params.job_name = jobName
    if (graphType) params.graph_type = graphType
    return request.get('/job-graph/full-graph', { params })
  }
}

from fastapi import APIRouter, Query
from typing import Optional, Literal
from app.services.neo4j_service import neo4j_service

router = APIRouter(prefix="/job-graph", tags=["岗位图谱"])


@router.get("/jobs")
def get_all_jobs():
    jobs = neo4j_service.get_all_jobs()
    return {"data": jobs}


@router.get("/jobs-with-paths")
def get_jobs_with_paths():
    jobs = neo4j_service.get_jobs_with_paths()
    return {"data": jobs}


@router.get("/promotion-paths")
def get_promotion_paths(job_name: str = Query(..., description="岗位名称")):
    result = neo4j_service.get_promotion_paths(job_name)
    return {"data": result}


@router.get("/transfer-paths")
def get_transfer_paths(job_name: str = Query(..., description="岗位名称")):
    result = neo4j_service.get_transfer_paths(job_name)
    return {"data": result}


@router.get("/full-graph")
def get_full_career_graph(
    job_name: Optional[str] = Query(None, description="岗位名称（可选）"),
    graph_type: Literal["all", "promotion", "transfer"] = Query("all", description="图谱类型：all/promotion/transfer")
):
    result = neo4j_service.get_full_career_graph(job_name, graph_type)
    return {"data": result}

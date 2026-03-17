from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class EducationItem(BaseModel):
    school: Optional[str] = None
    major: Optional[str] = None
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    description: Optional[str] = None


class ExperienceItem(BaseModel):
    company: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None


class ProjectItem(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = []


class SkillItem(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    category: Optional[str] = None


class CertificateItem(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiry_date: Optional[str] = None


class AwardItem(BaseModel):
    name: Optional[str] = None
    level: Optional[str] = None
    date: Optional[str] = None
    description: Optional[str] = None


class AbilityScores(BaseModel):
    professional_skills: int = Field(default=0, ge=0, le=100)
    learning_ability: int = Field(default=0, ge=0, le=100)
    communication: int = Field(default=0, ge=0, le=100)
    stress_resistance: int = Field(default=0, ge=0, le=100)
    innovation: int = Field(default=0, ge=0, le=100)
    internship_ability: int = Field(default=0, ge=0, le=100)


class StudentProfileCreate(BaseModel):
    basic_info: Dict[str, Any]
    education: Optional[List[EducationItem]] = []
    experience: Optional[List[ExperienceItem]] = []
    projects: Optional[List[ProjectItem]] = []
    skills: Optional[List[SkillItem]] = []
    certificates: Optional[List[CertificateItem]] = []
    awards: Optional[List[AwardItem]] = []


class StudentProfileUpdate(BaseModel):
    basic_info: Optional[Dict[str, Any]] = None
    education: Optional[List[EducationItem]] = None
    experience: Optional[List[ExperienceItem]] = None
    projects: Optional[List[ProjectItem]] = None
    skills: Optional[List[SkillItem]] = None
    certificates: Optional[List[CertificateItem]] = None
    awards: Optional[List[AwardItem]] = None


class StudentProfileResponse(BaseModel):
    id: int
    student_id: int
    basic_info: Dict[str, Any]
    education: Optional[List[Dict[str, Any]]] = []
    experience: Optional[List[Dict[str, Any]]] = []
    projects: Optional[List[Dict[str, Any]]] = []
    skills: Optional[List[Dict[str, Any]]] = []
    certificates: Optional[List[Dict[str, Any]]] = []
    awards: Optional[List[Dict[str, Any]]] = []
    ability_scores: Dict[str, int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeParseResponse(BaseModel):
    basic_info: Dict[str, Any]
    education: List[EducationItem]
    experience: List[ExperienceItem]
    projects: List[ProjectItem]
    skills: List[SkillItem]
    certificates: List[CertificateItem]
    awards: List[AwardItem]


class AbilityAssessmentResponse(BaseModel):
    ability_scores: AbilityScores
    summary: str

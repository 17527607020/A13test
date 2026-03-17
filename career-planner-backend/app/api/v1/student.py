from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.core.config import get_db
from app.schemas.student import (
    StudentProfileCreate, StudentProfileUpdate, StudentProfileResponse,
    ResumeParseResponse, AbilityAssessmentResponse, AbilityScores
)
from app.models.student import Student, StudentProfile
import json
import httpx

router = APIRouter(prefix="/students", tags=["学生画像"])


@router.post("/resume/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """
    上传简历文件，调用AI解析
    """
    try:
        content = await file.read()
        file_type = file.content_type
        
        if file_type == "application/pdf":
            text_content = await extract_text_from_pdf(content)
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/msword"]:
            text_content = await extract_text_from_docx(content)
        elif file_type in ["image/jpeg", "image/png"]:
            text_content = await extract_text_from_image(content)
        else:
            raise HTTPException(status_code=400, detail="不支持的文件格式")
        
        parsed_data = await parse_resume_with_ai(text_content)
        
        return {
            "success": True,
            "data": parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"简历解析失败: {str(e)}")


@router.post("/resume/parse")
async def parse_resume_text(
    text: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    """
    单独调用AI解析简历文本
    """
    try:
        parsed_data = await parse_resume_with_ai(text)
        return {
            "success": True,
            "data": parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"简历解析失败: {str(e)}")


@router.get("/profile")
async def get_student_profile(
    user_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """
    获取当前登录学生的最新画像
    """
    try:
        if user_id:
            result = await db.execute(
                select(StudentProfile).where(StudentProfile.student_id == user_id).order_by(StudentProfile.updated_at.desc()).limit(1)
            )
        else:
            result = await db.execute(select(StudentProfile).order_by(StudentProfile.updated_at.desc()).limit(1))
        
        profile = result.scalar_one_or_none()
        
        if not profile:
            return {
                "success": True,
                "data": None,
                "message": "暂无学生画像数据"
            }
        
        return {
            "success": True,
            "data": profile
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取学生画像失败: {str(e)}")


@router.post("/profile")
async def create_or_update_profile(
    profile_data: StudentProfileCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    创建或更新学生画像
    """
    try:
        from app.models.user import User
        
        username = "test_user"
        
        result = await db.execute(
            select(User).where(User.username == username)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        result = await db.execute(
            select(Student).where(Student.user_id == user.id)
        )
        student = result.scalar_one_or_none()
        
        if not student:
            raise HTTPException(status_code=404, detail="学生不存在")
        
        existing_profile = await db.execute(
            select(StudentProfile).where(StudentProfile.student_id == student.id)
        )
        existing = existing_profile.scalar_one_or_none()
        
        ability_assessment = await assess_ability(profile_data)
        
        profile_dict = {
            "student_id": student.id,
            "basic_info": profile_data.basic_info,
            "education": [edu.dict() for edu in profile_data.education],
            "experience": [exp.dict() for exp in profile_data.experience],
            "projects": [proj.dict() for proj in profile_data.projects],
            "skills": [skill.dict() for skill in profile_data.skills],
            "certificates": [cert.dict() for cert in profile_data.certificates],
            "awards": [award.dict() for award in profile_data.awards],
            "ability_scores": ability_assessment.ability_scores.dict()
        }
        
        if existing:
            for key, value in profile_dict.items():
                setattr(existing, key, value)
            await db.commit()
            await db.refresh(existing)
            
            response_data = {
                "id": existing.id,
                "student_id": existing.student_id,
                "basic_info": existing.basic_info,
                "education": existing.education,
                "experience": existing.experience,
                "projects": existing.projects,
                "skills": existing.skills,
                "certificates": existing.certificates,
                "awards": existing.awards,
                "ability_scores": existing.ability_scores,
                "created_at": existing.created_at,
                "updated_at": existing.updated_at
            }
            
            return {
                "success": True,
                "data": response_data,
                "message": "学生画像更新成功"
            }
        else:
            new_profile = StudentProfile(**profile_dict)
            db.add(new_profile)
            await db.commit()
            await db.refresh(new_profile)
            
            response_data = {
                "id": new_profile.id,
                "student_id": new_profile.student_id,
                "basic_info": new_profile.basic_info,
                "education": new_profile.education,
                "experience": new_profile.experience,
                "projects": new_profile.projects,
                "skills": new_profile.skills,
                "certificates": new_profile.certificates,
                "awards": new_profile.awards,
                "ability_scores": new_profile.ability_scores,
                "created_at": new_profile.created_at,
                "updated_at": new_profile.updated_at
            }
            
            return {
                "success": True,
                "data": response_data,
                "message": "学生画像创建成功"
            }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"保存学生画像失败: {str(e)}")


async def extract_text_from_pdf(content: bytes) -> str:
    """从PDF中提取文本"""
    try:
        import PyPDF2
        from io import BytesIO
        pdf_file = BytesIO(content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise Exception(f"PDF解析失败: {str(e)}")


async def extract_text_from_docx(content: bytes) -> str:
    """从Word文档中提取文本"""
    try:
        from docx import Document
        from io import BytesIO
        doc_file = BytesIO(content)
        doc = Document(doc_file)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        raise Exception(f"Word文档解析失败: {str(e)}")


async def extract_text_from_image(content: bytes) -> str:
    """从图片中提取文本（OCR）"""
    try:
        import pytesseract
        from PIL import Image
        from io import BytesIO
        image = Image.open(BytesIO(content))
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        return text
    except Exception as e:
        raise Exception(f"图片OCR识别失败: {str(e)}")


async def parse_resume_with_ai(text: str) -> ResumeParseResponse:
    """调用AI解析简历"""
    try:
        api_key = "sk-dc907b3e150c4f70ad148cf0041382b3"
        
        prompt = f"""
        请从以下简历文本中提取结构化信息，以JSON格式返回：

        简历内容：
        {text}

        请提取以下信息并返回JSON格式：
        {{
            "basic_info": {{
                "name": "姓名",
                "gender": "性别",
                "age": "年龄",
                "phone": "电话",
                "email": "邮箱",
                "location": "所在地"
            }},
            "education": [
                {{
                    "school": "学校名称",
                    "major": "专业",
                    "degree": "学位",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                    "gpa": "GPA",
                    "description": "描述"
                }}
            ],
            "experience": [
                {{
                    "company": "公司名称",
                    "position": "职位",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                    "description": "工作描述"
                }}
            ],
            "projects": [
                {{
                    "name": "项目名称",
                    "role": "角色",
                    "start_date": "开始日期",
                    "end_date": "结束日期",
                    "description": "项目描述",
                    "technologies": ["技术栈1", "技术栈2"]
                }}
            ],
            "skills": [
                {{
                    "name": "技能名称",
                    "level": "熟练度",
                    "category": "技能类别"
                }}
            ],
            "certificates": [
                {{
                    "name": "证书名称",
                    "issuer": "颁发机构",
                    "issue_date": "颁发日期",
                    "expiry_date": "过期日期"
                }}
            ],
            "awards": [
                {{
                    "name": "奖项名称",
                    "level": "级别",
                    "date": "获得日期",
                    "description": "描述"
                }}
            ]
        }}

        只返回JSON，不要其他说明文字。
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {"role": "system", "content": "你是一个专业的简历解析助手，擅长从简历中提取结构化信息。"},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                },
                timeout=60.0
            )
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            json_start = content.find("{")
            json_end = content.rfind("}") + 1
            json_str = content[json_start:json_end]
            
            parsed_data = json.loads(json_str)
            
            return ResumeParseResponse(**parsed_data)
            
    except Exception as e:
        raise Exception(f"AI解析失败: {str(e)}")


async def assess_ability(profile_data: StudentProfileCreate) -> AbilityAssessmentResponse:
    """基于规则的能力评估"""
    try:
        from app.services.ability_assessment import calculate_ability_scores
        
        profile_dict = {
            'basic_info': profile_data.basic_info,
            'education': [edu.dict() for edu in profile_data.education],
            'experience': [exp.dict() for exp in profile_data.experience],
            'projects': [proj.dict() for proj in profile_data.projects],
            'skills': [skill.dict() for skill in profile_data.skills],
            'certificates': [cert.dict() for cert in profile_data.certificates],
            'awards': [award.dict() for award in profile_data.awards]
        }
        
        scores = calculate_ability_scores(profile_dict)
        
        ability_scores = AbilityScores(**scores)
        
        return AbilityAssessmentResponse(
            ability_scores=ability_scores,
            summary="能力评估完成"
        )
            
    except Exception as e:
        raise Exception(f"能力评估失败: {str(e)}")

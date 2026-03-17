def calculate_ability_scores(student_data: dict) -> dict:
    """
    根据学生画像数据计算六个维度的能力得分
    """
    scores = {}
    
    scores['professional_skills'] = calculate_professional_skills(student_data)
    scores['learning_ability'] = calculate_learning_ability(student_data)
    scores['communication'] = calculate_communication(student_data)
    scores['stress_resistance'] = calculate_stress_resistance(student_data)
    scores['innovation'] = calculate_innovation(student_data)
    scores['internship_ability'] = calculate_internship_ability(student_data)
    
    return scores


def calculate_professional_skills(student_data: dict) -> int:
    """专业技能得分"""
    score = 40
    
    skills = student_data.get('skills', [])
    skilled_count = sum(1 for s in skills if s.get('level') in ['熟练', '精通'])
    score += min(skilled_count * 5, 20)
    
    education = student_data.get('education', [])
    if education:
        edu = education[0]
        gpa = edu.get('gpa', '')
        try:
            gpa_value = float(gpa) if gpa else 0
            if gpa_value >= 3.8:
                score += 10
            elif gpa_value >= 3.5:
                score += 5
        except:
            pass
        
        ranking = edu.get('ranking', '') or edu.get('description', '')
        if '前10%' in ranking or '10%' in ranking:
            score += 10
        elif '前20%' in ranking or '20%' in ranking:
            score += 5
    
    tech_keywords = ['Spring Boot', 'Vue', 'React', 'TensorFlow', 'Docker', 'Kubernetes', 
                     'Python', 'Java', 'JavaScript', 'MySQL', 'MongoDB', 'Redis', 'Git',
                     'Node.js', 'FastAPI', 'Spring', 'Django', 'Flask', 'TypeScript']
    
    project_desc = ' '.join([p.get('description', '') for p in student_data.get('projects', [])])
    internship_desc = ' '.join([i.get('description', '') for i in student_data.get('experience', [])])
    all_desc = project_desc + ' ' + internship_desc
    
    tech_found = sum(1 for tech in tech_keywords if tech in all_desc)
    score += min(tech_found * 2, 10)
    
    return min(score, 100)


def calculate_learning_ability(student_data: dict) -> int:
    """学习能力得分"""
    score = 0
    
    education = student_data.get('education', [])
    if education:
        edu = education[0]
        gpa = edu.get('gpa', '')
        try:
            gpa_value = float(gpa) if gpa else 0
            if gpa_value >= 3.8:
                score += 30
            elif gpa_value >= 3.5:
                score += 20
            elif gpa_value >= 3.0:
                score += 10
        except:
            pass
    
    awards = student_data.get('awards', [])
    academic_keywords = ['数学建模', '编程', '算法', '竞赛', 'ACM', '创新', '挑战杯', '电子设计']
    for award in awards:
        award_name = award.get('name', '')
        level = award.get('level', '')
        if any(kw in award_name for kw in academic_keywords):
            if level in ['国家级', '省级']:
                score += 10
            else:
                score += 5
    
    score = min(score, 30)
    
    skills = student_data.get('skills', [])
    skill_count = len(skills)
    if skill_count >= 8:
        score += 15
    elif skill_count >= 5:
        score += 10
    
    return min(score, 100)


def calculate_communication(student_data: dict) -> int:
    """沟通能力得分"""
    score = 30
    
    keywords = ['沟通', '协调', '汇报', '讲解', '展示', '演示', '讲解', '团队', '合作', '协作']
    
    project_desc = ' '.join([p.get('description', '') + ' ' + p.get('role', '') for p in student_data.get('projects', [])])
    internship_desc = ' '.join([i.get('description', '') + ' ' + i.get('position', '') for i in student_data.get('experience', [])])
    all_desc = project_desc + ' ' + internship_desc
    
    keyword_count = sum(1 for kw in keywords if kw in all_desc)
    score += min(keyword_count * 3, 15)
    
    role_keywords = ['负责人', '组长', '主讲', '队长', '组织', '管理']
    if any(kw in all_desc for kw in role_keywords):
        score += 15
    
    education = student_data.get('education', [])
    if education:
        edu_desc = education[0].get('description', '')
        if any(kw in edu_desc for kw in ['学生干部', '学生会', '社团', '班长', '团支书']):
            score += 10
    
    return min(score, 100)


def calculate_stress_resistance(student_data: dict) -> int:
    """抗压能力得分"""
    score = 30
    
    keywords = ['高强度', '紧急', '多任务', 'deadline', '加班', '紧迫', '繁重', '同时', '并行']
    
    project_desc = ' '.join([p.get('description', '') for p in student_data.get('projects', [])])
    internship_desc = ' '.join([i.get('description', '') for i in student_data.get('experience', [])])
    all_desc = project_desc + ' ' + internship_desc
    
    keyword_count = sum(1 for kw in keywords if kw in all_desc)
    score += min(keyword_count * 3, 15)
    
    experiences = student_data.get('experience', [])
    for exp in experiences:
        start = exp.get('start_date', '')
        end = exp.get('end_date', '')
        if start and end:
            try:
                from datetime import datetime
                start_date = datetime.strptime(str(start)[:7], '%Y-%m')
                end_date = datetime.strptime(str(end)[:7], '%Y-%m')
                months = (end_date - start_date).days / 30
                if months >= 3:
                    score += 10
            except:
                pass
    
    score = min(score, 20)
    
    projects = student_data.get('projects', [])
    if len(projects) >= 3:
        score += 15
    elif len(projects) >= 2:
        score += 10
    
    return min(score, 100)


def calculate_innovation(student_data: dict) -> int:
    """创新能力得分"""
    score = 20
    
    keywords = ['创新', '优化', '改进', '新方法', '原创', '独特', '发明', '专利', '突破', '革新']
    
    project_desc = ' '.join([p.get('description', '') for p in student_data.get('projects', [])])
    internship_desc = ' '.join([i.get('description', '') for i in student_data.get('experience', [])])
    all_desc = project_desc + ' ' + internship_desc
    
    keyword_count = sum(1 for kw in keywords if kw in all_desc)
    score += min(keyword_count * 5, 20)
    
    awards = student_data.get('awards', [])
    innovation_keywords = ['创新', '专利', '发明', '挑战杯', '创客']
    for award in awards:
        award_name = award.get('name', '')
        if any(kw in award_name for kw in innovation_keywords):
            score += 15
    
    score = min(score, 30)
    
    if any(kw in all_desc for kw in ['上线', '商用', '用户', '实际应用', '落地', '部署']):
        score += 15
    
    return min(score, 100)


def calculate_internship_ability(student_data: dict) -> int:
    """实习能力得分"""
    score = 0
    
    experiences = student_data.get('experience', [])
    score += min(len(experiences) * 20, 60)
    
    famous_companies = ['腾讯', '阿里', '百度', '字节', '华为', '京东', '美团', '拼多多', 
                       '微软', 'Google', 'Amazon', 'Apple', 'Meta', 'IBM', 'Oracle',
                       '大厂', '500强', '上市公司', '互联网', 'BAT']
    
    for exp in experiences:
        company = exp.get('company', '')
        if any(fc in company for fc in famous_companies):
            score += 10
    
    score = min(score, 20)
    
    for exp in experiences:
        desc = exp.get('description', '')
        quant_keywords = ['提升', '减少', '优化', '提高', '增长', '降低', '独立负责', '主导', '完成']
        if any(kw in desc for kw in quant_keywords):
            score += 5
    
    score = min(score, 20)
    
    return min(score, 100)

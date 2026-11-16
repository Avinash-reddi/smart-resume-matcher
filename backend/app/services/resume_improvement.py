from backend.app.services.matcher import normalize_skill
from backend.app.services.skill_extractor import extract_skills


def analyze_resume_improvements(
    sections,
    skill_requirements,
    project_match
):
    improvements = []

    # 1. Professional Summary Analysis
    summary = sections.get("summary", "").strip()

    if not summary:
        improvements.append({
            "section": "Professional Summary",
            "status": "missing",
            "suggestion": "Add a professional summary highlighting your technical skills, experience, and career objectives."
        })

    elif len(summary.split()) < 30:
        improvements.append({
            "section": "Professional Summary",
            "status": "needs_improvement",
            "suggestion": "Expand your professional summary with relevant technical skills and project experience."
        })

    else:
        improvements.append({
            "section": "Professional Summary",
            "status": "good",
            "suggestion": "Your professional summary is present. Keep it relevant to the target job."
        })


    # 2. Technical Skills Analysis
    resume_skills_text = sections.get("skills", "")

    extracted_resume_skills = extract_skills(
        resume_skills_text
    )

    resume_skill_set = {
        normalize_skill(skill)
        for skills in extracted_resume_skills.values()
        for skill in skills
    }

    required_skills = skill_requirements.get(
        "required_skills", []
    )

    preferred_skills = skill_requirements.get(
        "preferred_skills", []
    )

    missing_required = [
        skill for skill in required_skills
        if normalize_skill(skill) not in resume_skill_set
    ]

    missing_preferred = [
        skill for skill in preferred_skills
        if normalize_skill(skill) not in resume_skill_set
    ]

    improvements.append({
        "section": "Technical Skills",
        "status": "needs_improvement" if missing_required else "good",
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "suggestion": (
            "Consider adding relevant missing required skills if you have experience with them."
            if missing_required
            else "Your listed technical skills cover the required skills."
        )
    })


    # 3. Project Analysis
    projects = sections.get("projects", "").strip()

    project_analysis = project_match.get(
        "project_analysis", []
    )

    if not projects:
        improvements.append({
            "section": "Projects",
            "status": "missing",
            "suggestion": "Add relevant technical projects demonstrating your practical skills."
        })

    elif not project_analysis:
        improvements.append({
            "section": "Projects",
            "status": "needs_improvement",
            "suggestion": "Review your project descriptions and include technologies, implementation details, and outcomes."
        })

    elif project_match.get("project_score", 0) < 25:
        improvements.append({
            "section": "Projects",
            "status": "needs_improvement",
            "suggestion": "Add or highlight projects that demonstrate skills relevant to the target job."
        })

    else:
        improvements.append({
            "section": "Projects",
            "status": "good",
            "suggestion": "Your projects show relevant technical skills. Highlight your contributions and measurable outcomes."
        })

    # 4. Experience Analysis
    experience = sections.get("experience", "").strip()

    if not experience:
        improvements.append({
            "section": "Experience",
            "status": "missing",
            "suggestion": "Add internships, work experience, or relevant practical training. If you are a fresher, highlight academic and personal projects."
        })

    else:
        improvements.append({
            "section": "Experience",
            "status": "good",
            "suggestion": "Include clear responsibilities, technologies used, and measurable achievements."
        })

    # 5. Resume Completeness
    important_sections = [
        "summary",
        "skills",
        "education",
        "projects"
    ]

    missing_sections = [
        section
        for section in important_sections
        if not sections.get(section, "").strip()
    ]

    improvements.append({
        "section": "Resume Completeness",
        "status": "needs_improvement" if missing_sections else "good",
        "missing_sections": missing_sections,
        "suggestion": (
            "Complete the missing resume sections."
            if missing_sections
            else "All essential resume sections are present."
        )
    })

    return {
        "total_checks": len(improvements),
        "improvements": improvements
    }

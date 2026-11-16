import time
from backend.app.services.ai_recommender import generate_recommendations
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pydantic import BaseModel
from backend.app.services.resume_improvement import (
    analyze_resume_improvements
)
from backend.app.services.resume_parser import (
    extract_text_from_pdf,
    extract_resume_sections
)
from backend.app.services.skill_extractor import extract_skills
from backend.app.services.job_parser import (
    extract_jd_skills,
    extract_required_and_preferred_skills
)
from backend.app.services.matcher import match_skills
from backend.app.services.project_matcher import match_projects
from backend.app.services.experience_parser import (
    extract_experience_requirement,
    evaluate_experience_requirement
)
from backend.app.services.education_parser import extract_education_requirement
from backend.app.services.education_matcher import evaluate_education_match
from backend.app.services.score_calculator import (
    calculate_skill_match_score,
    calculate_final_score
)
from backend.app.services.semantic_matcher import calculate_semantic_similarity

app = FastAPI(
    title="Smart Resume Job Matching Engine",
    description="AI-powered resume and job matching API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
class JobDescriptionRequest(BaseModel):
    job_description: str

@app.post("/job/description")
def extract_job_skills(request: JobDescriptionRequest):
    skills = extract_jd_skills(request.job_description)
    return {"skills": skills}

@app.post("/match")
def match_resume_to_job(
    resume_skills: dict,
    job_description: str
):
    jd_skills = extract_jd_skills(job_description)

    skill_requirements = extract_required_and_preferred_skills(
        job_description
    )

    result = match_skills(
        resume_skills,
        jd_skills
    )

    score = calculate_skill_match_score(
        result["matched_skills"],
        skill_requirements["required_skills"],
        skill_requirements["preferred_skills"]
    )

    return {
        "jd_skills": jd_skills,
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "match_score": score
    }

@app.get("/")
def home():
    return {
        "message": "Smart Resume Job Matching Engine is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    upload_directory = Path("data/resumes")
    upload_directory.mkdir(parents=True, exist_ok=True)

    file_path = upload_directory / file.filename

    content = await file.read()

    with open(file_path, "wb") as resume_file:
        resume_file.write(content)

    extracted_text = extract_text_from_pdf(str(file_path))
    sections = extract_resume_sections(str(file_path))
    skills = extract_skills(sections["skills"])

    return {
        "filename": file.filename,
        "message": "Resume uploaded successfully",
        "text": extracted_text,
        "sections": sections,
        "skills": skills
    }
@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    total_start = time.perf_counter()

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    upload_directory = Path("data/resumes")
    upload_directory.mkdir(parents=True, exist_ok=True)

    file_path = upload_directory / file.filename

    content = await file.read()

    with open(file_path, "wb") as resume_file:
        resume_file.write(content)

    start = time.perf_counter()
    extracted_text = extract_text_from_pdf(str(file_path))
    print(f"PDF extraction: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    sections = extract_resume_sections(str(file_path))
    print(f"Section extraction: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    resume_skills = extract_skills(
        sections["skills"]
    )
    print(f"Resume skill extraction: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    jd_skills = extract_jd_skills(
        job_description
    )
    skill_requirements = extract_required_and_preferred_skills(
        job_description
    )
    print("\n===== DEBUG: SKILL REQUIREMENTS =====")
    print(skill_requirements)
    print(f"JD parsing: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    result = match_skills(
        resume_skills,
        jd_skills
    )
    print(f"Skill matching: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    experience_requirement = extract_experience_requirement(
        job_description
    )
    experience_status = evaluate_experience_requirement(
        experience_requirement["required_years"],
        experience_requirement["fresher_allowed"]
    )
    print(f"Experience analysis: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    education_requirement = extract_education_requirement(
        job_description
    )
    education_match = evaluate_education_match(
        sections["education"],
        education_requirement
    )
    print(f"Education analysis: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    project_match = match_projects(
        sections["projects"],
        skill_requirements
    )
    print(f"Project matching: {time.perf_counter() - start:.2f}s")
    start = time.perf_counter()

    resume_improvement_analysis = analyze_resume_improvements(
        sections,
        skill_requirements,
        project_match
    )

    print(
        f"Resume improvement analysis: "
        f"{time.perf_counter() - start:.2f}s"
    )

    start = time.perf_counter()
    score = calculate_skill_match_score(
        result["matched_skills"],
        skill_requirements["required_skills"],
        skill_requirements["preferred_skills"]
    )
    print(f"Skill score: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    semantic_score = calculate_semantic_similarity(
        extracted_text,
        job_description
    )
    print(f"Semantic matching: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    final_score = calculate_final_score(
        score,
        semantic_score,
        project_match["project_score"]
    )
    print(f"Final score calculation: {time.perf_counter() - start:.2f}s")

    start = time.perf_counter()
    ai_recommendations = generate_recommendations(
        resume_skills,
        jd_skills,
        result["matched_skills"],
        result["missing_skills"],
        project_match,
        experience_status,
        education_match
    )
    print(f"AI recommendations: {time.perf_counter() - start:.2f}s")

    print(f"TOTAL ANALYZE TIME: {time.perf_counter() - total_start:.2f}s")
    print("================================")

    return {
        "filename": file.filename,
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "skill_requirements": skill_requirements,
        "experience_requirement": experience_requirement,
        "experience_status": experience_status,
        "education_requirement": education_requirement,
        "education_match": education_match,
        "project_match": project_match,
        "matched_skills": result["matched_skills"],
        "missing_skills": result["missing_skills"],
        "skill_match_score": score,
        "semantic_score": semantic_score,
        "final_match_score": final_score,
        "ai_recommendations": ai_recommendations,
        "resume_improvement_analysis": resume_improvement_analysis
    }
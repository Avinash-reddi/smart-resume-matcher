import re
SKILL_ALIASES = {
    "core java": "java",
    "java 8": "java",
    "java 8+": "java",
    "oop": "object-oriented programming",
    "object oriented programming": "object-oriented programming",
    "rest apis": "rest api",
    "restful api": "rest api",
    "restful apis": "rest api",
    "rest api design": "rest api",
    "restful api design": "rest api",
    "react.js": "react",
    "reactjs": "react",
    "html5": "html",
    "css3": "css",
    "postgres": "postgresql",
    "git hub": "github",
    "aws services": "aws",
    "spring frameworks": "spring framework",
    "microservices architecture": "microservices",
    "javascript (es6+)": "javascript",
    "javascript es6+": "javascript",
        # AI terminology normalization
    "large language models": "llms",
    "ai agent": "ai agents",
    "agents": "ai agents",
    "openai": "openai api",
    "anthropic": "anthropic api",
    "gemini": "gemini api",
    "retrieval augmented generation": "rag",
    "retrieval-augmented generation": "rag",
    "vector database": "vector databases",
    "embedding": "embeddings",
}


def normalize_skill(skill):
    skill = skill.lower().strip()

    # Remove proficiency labels.
    skill = re.sub(
        r"\s*\((basics|basic|beginner|intermediate|advanced)\)\s*",
        "",
        skill
    )

    skill = re.sub(r"\s+", " ", skill)

    skill = SKILL_ALIASES.get(skill, skill)

    return skill


def match_skills(resume_skills, jd_skills):
    resume_skill_set = set()

    for skills in resume_skills.values():
        for skill in skills:
            normalized_skill = normalize_skill(skill)

            resume_skill_set.add(
                normalized_skill
            )

    jd_skill_set = {
        normalize_skill(skill)
        for skill in jd_skills
    }

    matched_skills = sorted(
        resume_skill_set.intersection(
            jd_skill_set
        )
    )

    missing_skills = sorted(
        jd_skill_set.difference(
            resume_skill_set
        )
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }
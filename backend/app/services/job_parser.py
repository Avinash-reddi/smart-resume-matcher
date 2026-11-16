
import re
from backend.app.services.matcher import normalize_skill

KNOWN_SKILLS = [
    # Programming Languages
    "java",
    "python",
    "javascript",
    "typescript",
    "c",
    "c++",
    "c#",
    "go",
    "kotlin",
    "swift",
    "sql",

    # Java / Backend
    "core java",
    "java 8",
    "java 8+",
    "spring",
    "spring framework",
    "spring boot",
    "spring security",
    "hibernate",
    "jpa",
    "maven",
    "gradle",

    # APIs / Architecture
    "rest api",
    "rest apis",
    "restful api",
    "restful apis",
    "graphql",
    "microservices",
    "http",
    "json",

    # Frontend
    "html",
    "html5",
    "css",
    "css3",
    "javascript",
    "react",
    "react.js",
    "reactjs",
    "typescript",
    "angular",
    "vue",
    "next.js",
    "node.js",
    "node",
    "dom",
    "responsive web design",

    # Database
    "sql",
    "mysql",
    "postgresql",
    "postgres",
    "mongodb",
    "redis",
    "oracle",
    "database",
    "database fundamentals",
    "database design",

    # Java Concepts
    "object-oriented programming",
    "object oriented programming",
    "oop",
    "collections framework",
    "exception handling",
    "data structures",
    "algorithms",

    # Development / Tools
    "git",
    "github",
    "gitlab",
    "jenkins",
    "docker",
    "kubernetes",
    "postman",
    "linux",
    "ci/cd",
    "continuous integration",
    "continuous deployment",

    # Testing
    "junit",
    "mockito",
    "pytest",
    "selenium",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # SDLC / Practices
    "sdlc",
    "agile",
    "software testing",
    "unit testing",
    "code review",

    
    # AI / Data
    "machine learning",
    "artificial intelligence",
    "deep learning",
    "natural language processing",
    "large language models",
    "llms",
    "prompt engineering",
    "ai apis",
    "openai api",
    "anthropic api",
    "gemini api",
    "fastapi",
    "flask",
    "embeddings",
    "vector databases",
    "vector database",
    "retrieval-augmented generation",
    "rag",
    "ai agents",
    "agents",
    "tool use",
    "automation",
    "openai",
    "anthropic",
    "gemini",
    # Computer Science Fundamentals
    "operating systems",
    "computer networks",
    "dbms",
    "problem solving",
    "system design",
    "software architecture",
    "code reviews",
    "query optimization",
    "automated testing",

    # Backend Development
    "express.js",
    "express",
    "api integration",


]


def extract_jd_skills(job_description: str):
    text = job_description.lower()

    found_skills = []

    for skill in sorted(KNOWN_SKILLS, key=len, reverse=True):
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    filtered_skills = []

    for skill in found_skills:
        is_duplicate = False

        for other in found_skills:
            if skill == other:
                continue

            pattern = (
                r"(?<!\w)"
                + re.escape(skill)
                + r"(?!\w)"
            )

            if re.search(pattern, other):
                is_duplicate = True
                break

        if not is_duplicate:
            filtered_skills.append(skill)

    normalized_skills = [
        normalize_skill(skill)
        for skill in filtered_skills
    ]



    return sorted(set(normalized_skills))

def extract_required_and_preferred_skills(job_description: str):
    text = job_description.lower()

    all_skills = extract_jd_skills(job_description)

    preferred_headings = [
        "preferred skills",
        "preferred technical skills",
        "preferred qualifications",
        "nice to have",
        "nice-to-have",
        "desired skills",
        "bonus skills",
        "additional skills",
        "what would make you stand out"
    ]

    required_headings = [
        "required skills",
        "required technical skills",
        "mandatory skills",
        "must have",
        "must-have",
        "qualifications",
        "requirements"
    ]

    preferred_positions = []

    for heading in preferred_headings:
        start = 0

        while True:
            index = text.find(heading, start)

            if index == -1:
                break

            preferred_positions.append(index)
            start = index + len(heading)

    preferred_positions.sort()

    preferred_section = ""

    if preferred_positions:
        preferred_start = preferred_positions[0]

        next_sections = []

        for heading in (
            required_headings + preferred_headings
        ):
            index = text.find(
                heading,
                preferred_start + 1
            )

            if index != -1:
                next_sections.append(index)

        if next_sections:
            preferred_end = min(next_sections)
        else:
            preferred_end = len(text)

        preferred_section = text[
            preferred_start:preferred_end
        ]

    preferred_section_skills = set(
        extract_jd_skills(preferred_section)
    )

    preferred_skills = [
        skill
        for skill in all_skills
        if skill in preferred_section_skills
    ]

    required_skills = [
        skill
        for skill in all_skills
        if skill not in preferred_skills
    ]

    return {
        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),
        "all_skills": sorted(all_skills)
    }
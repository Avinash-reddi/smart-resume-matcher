import re

from backend.app.services.matcher import normalize_skill

PROJECT_SKILL_ALIASES = {
    "ai agents": [
        "ai agent",
        "ai agents"
    ],
    "tool use": [
        "tool use",
        "tool calling",
        "tool usage"
    ],
    "vector databases": [
        "vector database",
        "vector databases"
    ]
}
def split_projects(projects_text):
    lines = projects_text.splitlines()

    projects = []
    current_project = []

    def is_project_heading(line):
        line = line.strip()

        if not line:
            return False

        if line.startswith("•") or line.startswith("â€¢"):
            return False

        if line.endswith((".", ",", ";", ":")):
            return False

        words = line.split()

        if len(words) < 2 or len(words) > 12:
            return False

        lowercase_starters = {
            "as",
            "and",
            "with",
            "to",
            "for",
            "of",
            "in",
            "on",
            "by",
            "from",
            "using",
            "which",
            "that",
            "where",
            "while"
        }

        if words[0].lower() in lowercase_starters:
            return False

        return True

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if is_project_heading(line):
            if current_project:
                projects.append("\n".join(current_project))

            current_project = [line]

        else:
            current_project.append(line)

    if current_project:
        projects.append("\n".join(current_project))

    return [
        project.strip()
        for project in projects
        if project.strip()
    ]

def get_project_match_level(score):
    if score >= 50:
        return "Strong Match"

    if score >= 25:
        return "Partial Match"

    return "Low Match"


def match_projects(projects_text, skill_requirements):
    if not projects_text:
        return {
            "matched_projects": [],
            "project_skill_matches": {},
            "project_analysis": [],
            "project_score": 0,
            "best_matching_project": None,
            "project_suggestion": None
        }

    projects = split_projects(projects_text)

    required_skills = {
        normalize_skill(skill)
        for skill in skill_requirements["required_skills"]
    }

    preferred_skills = {
        normalize_skill(skill)
        for skill in skill_requirements["preferred_skills"]
    }

    all_skills = required_skills | preferred_skills

    project_analysis = []
    matched_projects = []
    project_skill_matches = {}

    for project in projects:
        project_lines = project.splitlines()
        project_name = project_lines[0].strip()
        project_lower = project.lower()

        matched_required = set()
        matched_preferred = set()

        for skill in all_skills:
            skill_variants = PROJECT_SKILL_ALIASES.get(
                skill,
                [skill]
            )

            for variant in skill_variants:
                pattern = (
                    r"(?<!\w)"
                    + re.escape(variant)
                    + r"(?!\w)"
                )

                if re.search(pattern, project_lower):
                    if skill in required_skills:
                        matched_required.add(skill)

                    if skill in preferred_skills:
                        matched_preferred.add(skill)

                    break

        matched_skills = sorted(
            matched_required | matched_preferred
        )

        # Calculate weighted project relevance.
        if required_skills and preferred_skills:
            project_score = (
                (len(matched_required) / len(required_skills)) * 70
                +
                (len(matched_preferred) / len(preferred_skills)) * 30
            )

        elif required_skills:
            project_score = (
                len(matched_required) / len(required_skills)
            ) * 100

        elif preferred_skills:
            project_score = (
                len(matched_preferred) / len(preferred_skills)
            ) * 100

        else:
            project_score = 0

        project_score = round(
            min(project_score, 100),
            2
        )

        project_analysis.append({
            "name": project_name,
            "matched_skills": matched_skills,
            "match_score": project_score,
            "match_level": get_project_match_level(project_score)
        })

        if matched_skills:
            matched_projects.append(project_name)
            project_skill_matches[project_name] = matched_skills

    project_analysis.sort(
        key=lambda project: project["match_score"],
        reverse=True
    )

    best_matching_project = None

    if project_analysis:
        best_project = project_analysis[0]

        if best_project["matched_skills"]:
            best_matching_project = best_project["name"]

    project_score = 0

    if project_analysis:
        project_score = project_analysis[0]["match_score"]

    project_suggestion = None

    if project_analysis and project_score < 25:
        matched_all_project_skills = set()

        for project in project_analysis:
            matched_all_project_skills.update(
                project["matched_skills"]
            )

        missing_project_skills = sorted(
            all_skills - matched_all_project_skills
        )

        project_suggestion = {
            "reason": "No existing project has a strong match with the job requirements.",
            "recommended_skills": missing_project_skills
        }

    return {
        "matched_projects": matched_projects,
        "project_skill_matches": project_skill_matches,
        "project_analysis": project_analysis,
        "project_score": project_score,
        "best_matching_project": best_matching_project,
        "project_suggestion": project_suggestion
    }

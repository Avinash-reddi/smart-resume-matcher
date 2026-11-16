def calculate_skill_match_score(
    matched_skills,
    required_skills,
    preferred_skills
):
    required_skills = {
        skill.lower().strip()
        for skill in required_skills
    }

    preferred_skills = {
        skill.lower().strip()
        for skill in preferred_skills
    }

    matched_skills = {
        skill.lower().strip()
        for skill in matched_skills
    }

    required_matched = (
        matched_skills.intersection(required_skills)
    )

    preferred_matched = (
        matched_skills.intersection(preferred_skills)
    )

    required_score = 0

    if required_skills:
        required_score = (
            len(required_matched)
            / len(required_skills)
        ) * 80

    preferred_score = 0

    if preferred_skills:
        preferred_score = (
            len(preferred_matched)
            / len(preferred_skills)
        ) * 20

    score = required_score + preferred_score

    return round(score, 2) 


def calculate_final_score(
    skill_score,
    semantic_score,
    project_score
):
    final_score = (
        skill_score * 0.60
        + semantic_score * 0.20
        + project_score * 0.20
    )

    return round(final_score, 2)
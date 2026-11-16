import re


def extract_experience_requirement(job_description: str):
    text = job_description.lower()

    fresher_keywords = [
        "fresher",
        "freshers",
        "fresh graduate",
        "fresh graduates",
        "entry level",
        "entry-level",
        "0 years",
        "0-1 years",
        "0–1 years"
    ]

    for keyword in fresher_keywords:
        if keyword in text:
            return {
                "required_years": 0,
                "fresher_allowed": True
            }

    patterns = [
        r"(\d+)\+?\s*(?:years|yrs)\s+of\s+experience",
        r"minimum\s+(\d+)\s*(?:years|yrs)",
        r"at\s+least\s+(\d+)\s*(?:years|yrs)",
        r"(\d+)\+?\s*(?:years|yrs)\s+experience"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return {
                "required_years": int(match.group(1)),
                "fresher_allowed": False
            }

    return {
        "required_years": 0,
        "fresher_allowed": True
    }
def evaluate_experience_requirement(
    required_years,
    fresher_allowed
):
    if fresher_allowed or required_years == 0:
        return {
            "status": "eligible",
            "message": "Fresher or entry-level candidates are accepted."
        }

    return {
        "status": "experience_required",
        "message": f"This role requires at least {required_years} years of experience."
    }
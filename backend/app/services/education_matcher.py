def evaluate_education_match(resume_education, education_requirement):
    required_degree = education_requirement["required_degree"]
    required_fields = education_requirement["required_fields"]

    if not required_degree and not required_fields:
        return {
            "status": "not_specified",
            "message": "The job description does not specify an education requirement."
        }

    education_text = resume_education.lower()

    degree_match = True
    field_matches = []

    if required_degree:
        degree_keywords = {
            "bachelor": [
                "b.tech",
                "btech",
                "b.e",
                "bachelor"
            ],
            "master": [
                "m.tech",
                "mtech",
                "m.e",
                "master",
                "mba",
                "mca"
            ],
            "phd": [
                "phd",
                "doctorate"
            ]
        }

        degree_match = any(
            keyword in education_text
            for keyword in degree_keywords.get(required_degree, [])
        )

    for field in required_fields:
        if field in education_text:
            field_matches.append(field)

    field_match = (
        not required_fields
        or len(field_matches) > 0
    )

    if degree_match and field_match:
        return {
            "status": "matched",
            "degree_match": degree_match,
            "field_matches": field_matches
        }

    return {
        "status": "gap",
        "degree_match": degree_match,
        "field_matches": field_matches
    }
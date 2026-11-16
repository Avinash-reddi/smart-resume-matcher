import re


DEGREE_PATTERNS = {
    "bachelor": [
        "bachelor",
        "b.tech",
        "btech",
        "b.e",
        "be",
        "undergraduate"
    ],
    "master": [
        "master",
        "m.tech",
        "mtech",
        "m.e",
        "me",
        "postgraduate",
        "mba",
        "mca"
    ],
    "phd": [
        "phd",
        "doctorate",
        "doctoral"
    ]
}


FIELD_KEYWORDS = [
    "computer science",
    "computer science engineering",
    "information technology",
    "software engineering",
    "electronics",
    "electrical",
    "mechanical",
    "civil",
    "data science",
    "artificial intelligence"
]


def extract_education_requirement(job_description: str):
    text = job_description.lower()

    required_degree = None

    for degree, patterns in DEGREE_PATTERNS.items():
        for pattern in patterns:
            if re.search(r"(?<!\w)" + re.escape(pattern) + r"(?!\w)", text):
                required_degree = degree
                break

        if required_degree:
            break

    required_fields = []

    for field in FIELD_KEYWORDS:
        if field in text:
            required_fields.append(field)

    return {
        "required_degree": required_degree,
        "required_fields": sorted(set(required_fields))
    }
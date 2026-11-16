import re


SECTION_NAMES = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective"
    ],
    "skills": [
        "skills",
        "technical skills",
        "technical skill",
        "core skills"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "internships",
        "internship",
        "work history"
    ],
    "education": [
        "education",
        "academic background",
        "qualifications"
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects"
    ],
    "certifications": [
        "certifications",
        "certificates",
        "certification"
    ]
}


def normalize_heading(line: str) -> str:
    line = line.lower().strip()
    line = re.sub(r"[^a-zA-Z\s]", "", line)
    line = re.sub(r"\s+", " ", line)
    return line


def detect_section(line: str):
    normalized_line = normalize_heading(line)

    for section, headings in SECTION_NAMES.items():
        if normalized_line in headings:
            return section

    return None


def parse_sections(text: str):
    sections = {
        "summary": [],
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": [],
        "other": []
    }

    current_section = "other"

    for line in text.splitlines():
        line = line.strip()

        if not line:
            if current_section == "projects":
                sections[current_section].append("")

            continue

        detected_section = detect_section(line)

        if detected_section:
            current_section = detected_section
        else:
            sections[current_section].append(line)

    for section in sections:
        sections[section] = "\n".join(sections[section])

    return sections
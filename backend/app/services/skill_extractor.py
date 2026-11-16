def extract_skills(skills_text: str):
    skills = {}

    category_aliases = {
        "data structures & algorithms": [
            "data structures",
            "algorithms"
        ],
        "oops": [
            "object-oriented programming"
        ]
    }

    for line in skills_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if ":" not in line:
            continue

        category, values = line.split(":", 1)

        category = category.strip().lower()
        values = values.strip()

        skill_list = [
            skill.strip()
            for skill in values.split(",")
            if skill.strip()
        ]

        skills[category] = skill_list

        # Recognize explicitly mapped category headings.
        if category in category_aliases:
            for skill in category_aliases[category]:
                skill_list.append(skill)

    return skills
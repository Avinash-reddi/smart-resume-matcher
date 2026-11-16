
import json
import subprocess
import time


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"


def generate_recommendations(
    resume_skills,
    jd_skills,
    matched_skills,
    missing_skills,
    project_match,
    experience_status,
    education_match
):
    important_missing = missing_skills[:6]
    important_matched = matched_skills[:6]

    prompt = f"""
You are a resume improvement assistant.

Matched skills: {important_matched}
Missing skills: {important_missing}
Project score: {project_match.get("project_score", 0)}
Experience: {experience_status.get("status", "not_specified")}
Education: {education_match.get("status", "not_specified")}

Generate exactly four sections:

1. Skill Gaps:
List up to 6 missing skills.

2. Project Recommendations:
Suggest 2 practical projects using missing skills.

3. Resume Improvements:
Give 3 specific improvements.

4. Learning Priorities:
List 5 skills in priority order.

Keep every point short.
Do not invent experience or achievements.
"""

    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 2048,
            "num_predict": 200,
            "temperature": 0.2
        }
    }

    start = time.perf_counter()

    try:
        result = subprocess.run(
            [
                "curl.exe",
                "-sS",
                "--max-time", "120",
                "-X", "POST",
                "-H", "Content-Type: application/json",
                "--data-binary", "@-",
                OLLAMA_URL
            ],
            input=json.dumps(data),
            capture_output=True,
            text=True,
            timeout=125
        )

        print(
            "DIRECT CURL TIME:",
            round(time.perf_counter() - start, 2),
            "seconds"
        )
        print("CURL RETURN CODE:", result.returncode)

        if result.returncode != 0:
            print("CURL STDERR:", repr(result.stderr))
            return "AI recommendations are temporarily unavailable."

        response_data = json.loads(result.stdout)

        print("OLLAMA LOAD TIME:", response_data.get("load_duration", 0) / 1e9, "seconds")
        print("OLLAMA PROMPT TIME:", response_data.get("prompt_eval_duration", 0) / 1e9, "seconds")
        print("OLLAMA GENERATION TIME:", response_data.get("eval_duration", 0) / 1e9, "seconds")
        print("OLLAMA GENERATED TOKENS:", response_data.get("eval_count", 0))


        return response_data.get("response", "").strip()

    except subprocess.TimeoutExpired:
        print("AI ERROR: Request timed out")
        return "AI recommendations are temporarily unavailable because the local AI model took too long to respond."

    except Exception as e:
        print("AI ERROR:", repr(e))
        return "AI recommendations are temporarily unavailable."

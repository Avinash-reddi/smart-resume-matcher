# Smart Resume Matcher

An AI-powered resume and job description matching application built with **React, FastAPI, Python, and NLP**. It analyzes resumes against job descriptions and provides skill matching, semantic similarity, project analysis, and resume improvement recommendations.

## Features

- **Resume Upload:** Upload PDF resumes and extract text.
- **Resume Parsing:** Identify skills, education, experience, and projects.
- **Job Description Analysis:** Extract required and preferred skills.
- **Skill Matching:** Identify matched and missing skills.
- **Semantic Matching:** Compare resume and job description meaning using sentence embeddings.
- **Project Analysis:** Evaluate project relevance to the job description.
- **Experience & Education Analysis:** Check eligibility against job requirements.
- **Match Score:** Calculate an overall resume-job compatibility score.
- **Resume Improvement:** Identify areas where the resume can be improved.
- **AI Recommendations:** Generate recommendations using a local Ollama model.

## Tech Stack

**Frontend**
- React
- Vite
- JavaScript
- CSS

**Backend**
- Python
- FastAPI
- Uvicorn
- PyMuPDF
- Scikit-learn
- Sentence Transformers

**AI / NLP**
- Sentence Transformers (`all-MiniLM-L6-v2`)
- Ollama (`qwen2.5-coder:7b`)

**Tools**
- Git
- GitHub
- VS Code

## Project Structure

```text
smart-resume-matcher/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   └── services/
│   │       ├── ai_recommender.py
│   │       ├── education_matcher.py
│   │       ├── education_parser.py
│   │       ├── experience_parser.py
│   │       ├── job_parser.py
│   │       ├── matcher.py
│   │       ├── project_matcher.py
│   │       ├── resume_improvement.py
│   │       ├── resume_parser.py
│   │       ├── score_calculator.py
│   │       ├── section_parser.py
│   │       ├── semantic_matcher.py
│   │       ├── skill_extractor.py
│   │       └── text_cleaner.py
│   │
│   └── requirements.txt
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   └── resumes/
│
├── .gitignore
└── README.md
```

## Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or later
- Node.js and npm
- Git
- Ollama (for local AI recommendations)

### 1. Clone the Repository

```bash
git clone https://github.com/Avinash-reddi/smart-resume-matcher.git
cd smart-resume-matcher
```

### 2. Backend Setup

Create a Python virtual environment:

**Windows PowerShell:**

```powershell
python -m venv venv
```

Activate the environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
python -m pip install -r backend/requirements.txt
```

Start the FastAPI backend:

```powershell
python -m uvicorn app.main:app --reload --app-dir backend
```

Backend URL:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 3. Frontend Setup

Open a second terminal:

```powershell
cd frontend
```

Install dependencies:

```powershell
npm install
```

Start the React development server:

```powershell
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

### 4. Ollama Setup

Install Ollama and download the required model:

```bash
ollama pull qwen2.5-coder:7b
```

Make sure the Ollama service is running before using AI recommendations. The application connects to the local Ollama API.

### 5. Run the Complete Application

Run the following services in separate terminals:

| Service | Command |
|---|---|
| Backend | `python -m uvicorn app.main:app --reload --app-dir backend` |
| Frontend | `npm run dev` (inside `frontend`) |
| Ollama | Ensure the Ollama service is running |

Open the frontend at `http://localhost:5173`.

## How It Works

1. Upload a resume in PDF format.
2. Enter the job description.
3. The backend extracts resume and job description information.
4. The application identifies required, preferred, matched, and missing skills.
5. NLP-based semantic similarity evaluates the relevance of the resume.
6. Project, experience, and education details are analyzed.
7. The dashboard displays the overall match score and improvement recommendations.

## Future Improvements

- Cloud deployment of frontend and backend.
- Improved AI-powered resume recommendations.
- Support for additional resume formats.
- Enhanced job-role matching and analysis.

## Author

**Ganjikunta Avinash Reddy**

GitHub: https://github.com/Avinash-reddi


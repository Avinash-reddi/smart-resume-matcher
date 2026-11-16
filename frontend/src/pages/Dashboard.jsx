import ResumeImprovement from "../components/ResumeImprovement/ResumeImprovement"
import { useState } from "react"
import ResumeUpload from "../components/ResumeUpload/ResumeUpload"
import JobDescription from "../components/JobDescription/JobDescription"
import MatchScore from "../components/MatchScore/MatchScore"
import SkillAnalysis from "../components/SkillAnalysis/SkillAnalysis"
import ProjectAnalysis from "../components/ProjectAnalysis/ProjectAnalysis"
import ExperienceEducation from "../components/ExperienceEducation/ExperienceEducation"
import AIRecommendations from "../components/AIRecommendations/AIRecommendations"
import "./Dashboard.css"
import { analyzeResume } from "../services/api"


function Dashboard() {
  const [resumeFile, setResumeFile] = useState(null)
  const [jobDescription, setJobDescription] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [hasAnalyzed, setHasAnalyzed] = useState(false)
  const [error, setError] = useState("")
  const [analysisResult, setAnalysisResult] = useState(null)

  const handleAnalyze = async () => {
    setError("")
    setHasAnalyzed(false)

    if (!resumeFile) {
      setError("Please upload your resume.")
      return
    }

    if (!jobDescription.trim()) {
      setError("Please enter a job description.")
      return
    }

    setIsAnalyzing(true)

    try {
      const result = await analyzeResume(
        resumeFile,
        jobDescription
      )

      console.log("Analysis result:", result)

      setAnalysisResult(result)
      setHasAnalyzed(true)
    } catch (error) {
      setError(error.message)
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <div className="dashboard">
      <header className="header">
        <h1>Smart Resume Job Matcher</h1>
        <p>AI-powered resume and job description matching</p>
      </header>

      <main className="main-content">
        <section className="input-section">
          <ResumeUpload onFileSelect={setResumeFile} />

          <JobDescription
            onJobDescriptionChange={setJobDescription}
          />
        </section>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={isAnalyzing}
        >
          {isAnalyzing ? "Analyzing Resume..." : "Analyze Resume"}
        </button>

        {isAnalyzing && (
          <div className="loading-message">
            <div className="loading-spinner"></div>
            <p>
              Analyzing your resume and job description...
            </p>
          </div>
        )}

        {hasAnalyzed && !isAnalyzing && (
          <>
            <section className="results-section">
              <MatchScore
                score={analysisResult?.final_match_score ?? 0}
                skillScore={analysisResult?.skill_match_score ?? 0}
                semanticScore={analysisResult?.semantic_score ?? 0}
                projectScore={analysisResult?.project_match?.project_score ?? 0}
              />

              <SkillAnalysis
                matchedSkills={analysisResult?.matched_skills || []}
                missingSkills={analysisResult?.missing_skills || []}
              />

              <ProjectAnalysis
                projectMatch={analysisResult?.project_match}
              />

              <ExperienceEducation
                experienceStatus={analysisResult?.experience_status}
                experienceRequirement={analysisResult?.experience_requirement}
                educationMatch={analysisResult?.education_match}
                educationRequirement={analysisResult?.education_requirement}
              />
              <ResumeImprovement
                analysis={analysisResult?.resume_improvement_analysis}
              />
            </section>

            <AIRecommendations
              recommendations={analysisResult?.ai_recommendations || ""}
            />
          </>
        )}
      </main>
    </div>
  )
}

export default Dashboard
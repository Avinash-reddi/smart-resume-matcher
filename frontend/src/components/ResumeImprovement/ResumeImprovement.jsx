
import "./ResumeImprovement.css"

function ResumeImprovement({ analysis }) {
  const improvements = analysis?.improvements || []

  const getStatusLabel = (status) => {
    const labels = {
      good: "Good",
      missing: "Missing",
      needs_improvement: "Needs Improvement"
    }

    return labels[status] || "Not Evaluated"
  }

  const renderBadges = (items) => (
    <div className="improvement-skill-tags">
      {items.map((item) => (
        <span className="improvement-skill-tag" key={item}>
          {item}
        </span>
      ))}
    </div>
  )

  return (
    <section className="resume-improvement-section">
      <h2>Resume Improvement Analysis</h2>

      <p className="improvement-subtitle">
        Suggestions to improve your resume for this job description.
      </p>

      <div className="resume-improvement-grid">
        {improvements.map((item) => (
          <div className="result-card improvement-card" key={item.section}>
            <div className="improvement-header">
              <h3>{item.section}</h3>

              <span className={`improvement-status ${item.status}`}>
                {getStatusLabel(item.status)}
              </span>
            </div>

            <p>{item.suggestion}</p>

            {item.missing_required_skills?.length > 0 && (
              <div className="improvement-details">
                <strong>Missing Required Skills</strong>
                {renderBadges(item.missing_required_skills)}
              </div>
            )}

            {item.missing_preferred_skills?.length > 0 && (
              <div className="improvement-details">
                <strong>Missing Preferred Skills</strong>
                {renderBadges(item.missing_preferred_skills)}
              </div>
            )}

            {item.missing_sections?.length > 0 && (
              <div className="improvement-details">
                <strong>Missing Sections</strong>
                {renderBadges(item.missing_sections)}
              </div>
            )}
          </div>
        ))}
      </div>

      <p className="improvement-total">
        Total checks completed: {analysis?.total_checks ?? 0}
      </p>
    </section>
  )
}

export default ResumeImprovement

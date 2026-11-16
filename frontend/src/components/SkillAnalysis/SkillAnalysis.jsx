function SkillAnalysis({ matchedSkills = [], missingSkills = [] }) {
  return (
    <div className="result-card skill-analysis-card">
      <h2>Skills Analysis</h2>

      <div className="skill-summary">
        <span className="matched-count">
          {matchedSkills.length} Matched
        </span>

        <span className="missing-count">
          {missingSkills.length} Missing
        </span>
      </div>

      <h3>Matched Skills</h3>

      <div className="skill-list">
        {matchedSkills.map((skill) => (
          <span className="skill matched" key={skill}>
            {skill}
          </span>
        ))}
      </div>

      <h3>Missing Skills</h3>

      <div className="skill-list">
        {missingSkills.map((skill) => (
          <span className="skill missing" key={skill}>
            {skill}
          </span>
        ))}
      </div>
    </div>
  )
}

export default SkillAnalysis
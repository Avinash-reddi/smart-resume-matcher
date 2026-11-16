function ProjectAnalysis({ projectMatch }) {
  if (!projectMatch) {
    return (
      <div className="result-card project-analysis-card">
        <div className="project-header">
          <div>
            <h2>Project Analysis</h2>
            <p>How relevant your projects are to this job</p>
          </div>
        </div>

        <p>No project analysis available yet.</p>
      </div>
    )
  }

  const projects = projectMatch.project_analysis || []

  return (
    <div className="result-card project-analysis-card">
      <div className="project-header">
        <div>
          <h2>Project Analysis</h2>
          <p>How relevant your projects are to this job</p>
        </div>

        <div className="project-score">
          {projectMatch.project_score ?? 0}%
        </div>
      </div>

      {projectMatch.best_matching_project && (
        <div className="best-project">
          <span>Best Matching Project</span>
          <strong>
            {projectMatch.best_matching_project}
          </strong>
        </div>
      )}

      <div className="project-list">
        {projects.length === 0 ? (
          <p>No projects found.</p>
        ) : (
          projects.map((project) => (
            <div
              className="project-item"
              key={project.name}
            >
              <div className="project-info">
                <h3>{project.name}</h3>

                <div className="project-match-details">
                  <span>
                    {project.match_score}%
                  </span>

                  <span>
                    {project.match_level}
                  </span>
                </div>

                <div className="project-skills">
                  {project.matched_skills.length === 0 ? (
                    <span>No matching skills</span>
                  ) : (
                    project.matched_skills.map((skill) => (
                      <span key={skill}>
                        {skill}
                      </span>
                    ))
                  )}
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {projectMatch.project_suggestion && (
        <div className="project-suggestion">
          <h3>Project Recommendation</h3>

          <p>
            {projectMatch.project_suggestion.reason}
          </p>

          <div className="suggested-skills">
            {projectMatch.project_suggestion.recommended_skills.map(
              (skill) => (
                <span key={skill}>
                  {skill}
                </span>
              )
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProjectAnalysis
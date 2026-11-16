
function MatchScore({
  score = 0,
  skillScore = 0,
  semanticScore = 0,
  projectScore = 0
}) {
  const breakdown = [
    {
      name: "Skill Matching",
      score: skillScore,
      weight: 60
    },
    {
      name: "Semantic Similarity",
      score: semanticScore,
      weight: 20
    },
    {
      name: "Project Relevance",
      score: projectScore,
      weight: 20
    }
  ]

  return (
    <div className="result-card match-score-card">
      <h2>Match Score</h2>

      <div className="score-circle">
        <span>{score}%</span>
      </div>

      <p>Overall compatibility</p>

      <div className="score-breakdown">
        <h3>Job Match Explanation</h3>

        {breakdown.map((item) => (
          <div className="score-item" key={item.name}>
            <div className="score-item-header">
              <strong>{item.name}</strong>
              <span>{item.score}%</span>
            </div>

            <div className="score-bar">
              <div
                className="score-bar-fill"
                style={{ width: `${Math.min(100, Math.max(0, item.score))}%` }}
              />
            </div>

            <small>
              Weight: {item.weight}% | Contribution: {
                ((item.score * item.weight) / 100).toFixed(2)
              } points
            </small>
          </div>
        ))}
      </div>
    </div>
  )
}

export default MatchScore

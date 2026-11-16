
function formatRecommendation(text) {
  const lines = text.split("\n");

  return lines.map((line, index) => {
    const trimmed = line.trim();

    if (!trimmed) return null;

    // Section headings: 1. **Skill Gaps:**
    const headingMatch = trimmed.match(
      /^(\d+)\.\s+\*\*(.*?)\*\*:?\s*(.*)$/
    );

    if (headingMatch) {
      return (
        <div key={index} className="recommendation-block">
          <h3>
            {headingMatch[1]}. {headingMatch[2]}
          </h3>
          {headingMatch[3] && <p>{headingMatch[3]}</p>}
        </div>
      );
    }

    // Bold bullet: - **Java:** Description
    const boldBulletMatch = trimmed.match(
      /^[-•]\s+\*\*(.*?)\*\*:?\s*(.*)$/
    );

    if (boldBulletMatch) {
      return (
        <div key={index} className="recommendation-bullet">
          <strong>{boldBulletMatch[1]}</strong>
          {boldBulletMatch[2] && (
            <span> {boldBulletMatch[2]}</span>
          )}
        </div>
      );
    }

    // Normal bullet
    const simpleBulletMatch = trimmed.match(/^[-•]\s+(.*)$/);

    if (simpleBulletMatch) {
      return (
        <div key={index} className="recommendation-bullet">
          • {simpleBulletMatch[1]}
        </div>
      );
    }

    // Normal paragraph
    return <p key={index}>{trimmed}</p>;
  });
}

function AIRecommendations({ recommendations = "" }) {
  return (
    <section className="ai-section">
      <div className="ai-header">
        <div>
          <h2>AI Recommendations</h2>
          <p>
            Personalized suggestions based on your resume and the job description
          </p>
        </div>

        <span className="ai-badge">AI Powered</span>
      </div>

      <div className="recommendation-grid">
        <div className="recommendation-card">
          {recommendations ? (
            formatRecommendation(recommendations)
          ) : (
            <p>No AI recommendations available.</p>
          )}
        </div>
      </div>
    </section>
  );
}

export default AIRecommendations;

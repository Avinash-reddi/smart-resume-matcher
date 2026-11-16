function ExperienceEducation({
  experienceStatus,
  experienceRequirement,
  educationMatch,
  educationRequirement
}) {
  const experienceStatusValue =
    experienceStatus?.status || "not_specified"

  const educationStatus =
    educationMatch?.status || "not_specified"

  const educationFields =
    educationMatch?.field_matches || []

  const educationMessage =
    educationMatch?.message ||
    "Education requirement analysis"

  return (
    <div className="experience-education-grid">
      <div className="result-card">
        <h2>Experience</h2>

        <div
          className={`status-badge ${
            experienceStatusValue === "eligible"
              ? "eligible"
              : "not-eligible"
          }`}
        >
          {experienceStatusValue === "eligible"
            ? "Eligible"
            : "Not Eligible"}
        </div>

        <p>
          {experienceStatus?.message ||
            "Experience requirement analysis"}
        </p>

        <div className="info-row">
          <span>Required</span>

          <strong>
            {experienceRequirement?.required_years ?? 0} years
          </strong>
        </div>

        <div className="info-row">
          <span>Candidate Type</span>

          <strong>
            {experienceStatusValue === "eligible"
              ? "Fresher / Entry Level"
              : "Experienced"}
          </strong>
        </div>
      </div>

      <div className="result-card">
        <h2>Education</h2>

        <div
          className={`status-badge ${
            educationStatus === "matched"
              ? "matched"
              : educationStatus === "not_specified"
              ? "not-specified"
              : "not-matched"
          }`}
        >
          {educationStatus === "matched"
            ? "Matched"
            : educationStatus === "not_specified"
            ? "Not Specified"
            : "Not Matched"}
        </div>

        <p>{educationMessage}</p>

        <div className="info-row">
          <span>Required Degree</span>

          <strong>
            {educationRequirement?.required_degree ||
              "Not specified"}
          </strong>
        </div>

        <div className="info-row">
          <span>Matching Field</span>

          <strong>
            {educationFields.length > 0
              ? educationFields.join(", ")
              : "Not applicable"}
          </strong>
        </div>
      </div>
    </div>
  )
}

export default ExperienceEducation
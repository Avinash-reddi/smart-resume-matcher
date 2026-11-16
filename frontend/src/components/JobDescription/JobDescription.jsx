import { useState } from "react"

function JobDescription({ onJobDescriptionChange }) {
  const [jobDescription, setJobDescription] = useState("")

  const handleChange = (event) => {
    const value = event.target.value

    setJobDescription(value)
    onJobDescriptionChange(value)
  }

  return (
    <div className="card">
      <h2>Job Description</h2>
      <p>Paste the job description below</p>

      <textarea
        value={jobDescription}
        onChange={handleChange}
        placeholder="Paste the job description here..."
        rows="12"
      />

      <div className="character-count">
        {jobDescription.length} characters
      </div>
    </div>
  )
}

export default JobDescription
import { useState } from "react"

function ResumeUpload({ onFileSelect }) {
  const [fileName, setFileName] = useState("")

  const handleFileChange = (event) => {
    const file = event.target.files[0]

    if (!file) {
      setFileName("")
      onFileSelect(null)
      return
    }

    if (file.type !== "application/pdf") {
      setFileName("")
      onFileSelect(null)
      alert("Please select a PDF file.")
      return
    }

    setFileName(file.name)
    onFileSelect(file)
  }

  return (
    <div className="card">
      <h2>Upload Resume</h2>
      <p>Upload your resume in PDF format</p>

      <input
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
      />

      <div className="file-box">
        {fileName || "No resume selected"}
      </div>
    </div>
  )
}

export default ResumeUpload
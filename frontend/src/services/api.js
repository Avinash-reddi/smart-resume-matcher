const API_BASE_URL = "http://127.0.0.1:8000"

export async function analyzeResume(file, jobDescription) {
  const formData = new FormData()

  formData.append("file", file)
  formData.append("job_description", jobDescription)

  const response = await fetch(
    `${API_BASE_URL}/analyze`,
    {
      method: "POST",
      body: formData
    }
  )

  if (!response.ok) {
    const errorData = await response.json().catch(() => null)

    throw new Error(
      errorData?.detail || "Failed to analyze resume"
    )
  }

  return response.json()
}
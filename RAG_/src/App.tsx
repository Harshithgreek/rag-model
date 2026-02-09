import { useState, useRef } from 'react'
import { Upload, Send, FileText, Trash2, Loader2 } from 'lucide-react'
import './App.css'

interface Message {
  type: 'question' | 'answer'
  content: string
  sources?: string[]
}

function App() {
  const [file, setFile] = useState<File | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [question, setQuestion] = useState('')
  const [isUploading, setIsUploading] = useState(false)
  const [isAsking, setIsAsking] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([])
  const fileInputRef = useRef<HTMLInputElement>(null)

  const API_URL = 'http://localhost:8000'

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setIsUploading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_URL}/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData.detail || 'Upload failed')
      }

      const data = await response.json()
      setUploadedFiles(prev => [...prev, data.filename])
      setFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      alert('Document uploaded successfully!')
    } catch (error: any) {
      const msg = error?.message || 'Unknown error'
      alert(`Error uploading document: ${msg}\n\nMake sure the backend server is running on http://localhost:8000`)
      console.error('Upload error:', error)
    } finally {
      setIsUploading(false)
    }
  }

  const handleAskQuestion = async () => {
    if (!question.trim()) return

    const userMessage: Message = {
      type: 'question',
      content: question,
    }
    setMessages(prev => [...prev, userMessage])
    setQuestion('')
    setIsAsking(true)

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ question }),
      })

      if (!response.ok) {
        const errData = await response.json().catch(() => null)
        const detail = errData?.detail || 'Failed to get answer'
        throw new Error(detail)
      }

      const data = await response.json()
      const answerMessage: Message = {
        type: 'answer',
        content: data.answer,
        sources: data.source_documents,
      }
      setMessages(prev => [...prev, answerMessage])
    } catch (error) {
      const errorMessage: Message = {
        type: 'answer',
        content: error instanceof Error ? error.message : 'Error getting answer. Please make sure you have uploaded a document first and the backend server is running.',
      }
      setMessages(prev => [...prev, errorMessage])
      console.error(error)
    } finally {
      setIsAsking(false)
    }
  }

  const handleReset = async () => {
    if (!confirm('Are you sure you want to reset? This will delete all uploaded documents and conversation history.')) {
      return
    }

    try {
      await fetch(`${API_URL}/reset`, {
        method: 'DELETE',
      })
      setMessages([])
      setUploadedFiles([])
      setFile(null)
      if (fileInputRef.current) {
        fileInputRef.current.value = ''
      }
      alert('Reset successful!')
    } catch (error) {
      alert('Error resetting database')
      console.error(error)
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>📚 DOCUMIND RAG</h1>
        <p>Upload documents and ask questions about their content</p>
      </header>

      <div className="main-content">
        <div className="upload-section">
          <div className="upload-card">
            <h2>Upload Document</h2>
            <div className="upload-area">
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                onChange={handleFileSelect}
                className="file-input"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="file-label">
                <Upload className="icon" />
                <span>{file ? file.name : 'Choose PDF file'}</span>
              </label>
              <button
                onClick={handleUpload}
                disabled={!file || isUploading}
                className="btn btn-primary"
              >
                {isUploading ? (
                  <>
                    <Loader2 className="icon spinning" />
                    Uploading...
                  </>
                ) : (
                  <>
                    <Upload className="icon" />
                    Upload
                  </>
                )}
              </button>
            </div>

            {uploadedFiles.length > 0 && (
              <div className="uploaded-files">
                <h3>Uploaded Documents:</h3>
                <ul>
                  {uploadedFiles.map((filename, index) => (
                    <li key={index}>
                      <FileText className="icon-small" />
                      {filename}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <button onClick={handleReset} className="btn btn-danger">
              <Trash2 className="icon" />
              Reset All
            </button>
          </div>
        </div>

        <div className="chat-section">
          <div className="chat-card">
            <h2>Ask Questions</h2>
            <div className="messages-container">
              {messages.length === 0 ? (
                <div className="empty-state">
                  <p>Upload a document and start asking questions!</p>
                </div>
              ) : (
                messages.map((message, index) => (
                  <div key={index} className={`message message-${message.type}`}>
                    <div className="message-content">
                      {message.content}
                    </div>
                    {message.sources && message.sources.length > 0 && (
                      <div className="sources">
                        <strong>Sources:</strong>
                        <ul>
                          {message.sources.map((source, i) => (
                            <li key={i}>{source}</li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))
              )}
              {isAsking && (
                <div className="message message-answer">
                  <Loader2 className="icon spinning" />
                  <span>Thinking...</span>
                </div>
              )}
            </div>

            <div className="input-area">
              <input
                type="text"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAskQuestion()}
                placeholder="Ask a question about your documents..."
                className="question-input"
                disabled={isAsking}
              />
              <button
                onClick={handleAskQuestion}
                disabled={!question.trim() || isAsking}
                className="btn btn-primary"
              >
                <Send className="icon" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App

import { useState } from 'react'
import axios from 'axios'
import { API_URL } from '../config'

export default function Upload() {
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleUpload = async () => {
    if (!file) return

    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await axios.post(`${API_URL}/api/upload-syllabus`, formData)
      setMessage(response.data.message)
      
      // Gerar banco automaticamente
      await axios.post(`${API_URL}/api/generate-bank`, {
        min_questions_per_topic: 10
      })
      
      setMessage('Conteúdo programático recebido e banco de questões gerado!')
    } catch (error) {
      setMessage('Erro: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="card">
      <h1>Upload de Edital</h1>
      
      <div style={{ marginTop: '2rem' }}>
        <input
          type="file"
          accept=".txt,.pdf"
          onChange={(e) => setFile(e.target.files[0])}
        />
        
        <button
          className="btn btn-primary"
          onClick={handleUpload}
          disabled={!file || loading}
          style={{ marginLeft: '1rem' }}
        >
          {loading ? 'Processando...' : 'Upload'}
        </button>
      </div>
      
      {message && (
        <div style={{ marginTop: '1rem', padding: '1rem', background: '#d4edda', borderRadius: '4px' }}>
          {message}
        </div>
      )}
    </div>
  )
}

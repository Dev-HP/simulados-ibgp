import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import axios from 'axios'
import { API_URL } from '../config'

export default function SimuladoExec() {
  const { id } = useParams()
  const [simulado, setSimulado] = useState(null)
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [feedback, setFeedback] = useState(null)

  useEffect(() => {
    loadSimulado()
  }, [id])

  const loadSimulado = async () => {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/api/simulados/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    setSimulado(response.data)
  }

  const handleAnswer = async () => {
    if (!selectedAnswer) return

    const token = localStorage.getItem('token')
    const question = simulado.questions[currentQuestion]
    const response = await axios.post(`${API_URL}/api/simulados/${id}/answer`, {
      question_id: question.id,
      resposta: selectedAnswer
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })

    setFeedback(response.data)
  }

  const nextQuestion = () => {
    setCurrentQuestion(currentQuestion + 1)
    setSelectedAnswer(null)
    setFeedback(null)
  }

  if (!simulado) return <div>Carregando...</div>

  const question = simulado.questions[currentQuestion]
  if (!question) return <div>Simulado finalizado!</div>

  return (
    <div className="card">
      <div style={{ marginBottom: '2rem' }}>
        <span>Questão {currentQuestion + 1} de {simulado.questions.length}</span>
      </div>

      <div className="question-card">
        <h3>{question.enunciado}</h3>
        
        <div className="alternatives">
          {['A', 'B', 'C', 'D'].map((letter) => (
            <div
              key={letter}
              className={`alternative ${selectedAnswer === letter ? 'selected' : ''} ${
                feedback && letter === feedback.gabarito ? 'correct' : ''
              } ${
                feedback && selectedAnswer === letter && !feedback.is_correct ? 'incorrect' : ''
              }`}
              onClick={() => !feedback && setSelectedAnswer(letter)}
            >
              <strong>{letter})</strong> {question[`alternativa_${letter.toLowerCase()}`]}
            </div>
          ))}
        </div>

        {!feedback && (
          <button
            className="btn btn-primary"
            onClick={handleAnswer}
            disabled={!selectedAnswer}
            style={{ marginTop: '1rem' }}
          >
            Responder
          </button>
        )}

        {feedback && (
          <div style={{ marginTop: '1rem' }}>
            <div style={{
              padding: '1rem',
              background: feedback.is_correct ? '#d4edda' : '#f8d7da',
              borderRadius: '4px'
            }}>
              <strong>{feedback.is_correct ? '✓ Correto!' : '✗ Incorreto'}</strong>
              <p style={{ marginTop: '0.5rem' }}>{feedback.explicacao}</p>
              {feedback.referencia && (
                <p style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
                  Referência: {feedback.referencia}
                </p>
              )}
            </div>
            
            <button
              className="btn btn-primary"
              onClick={nextQuestion}
              style={{ marginTop: '1rem' }}
            >
              Próxima Questão
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

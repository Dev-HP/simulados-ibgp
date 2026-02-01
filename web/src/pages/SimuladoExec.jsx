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
  const [answers, setAnswers] = useState([]) // Armazenar todas as respostas
  const [showResult, setShowResult] = useState(false) // Mostrar resultado final

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
    
    // Armazenar resposta
    setAnswers([...answers, {
      question_id: question.id,
      resposta: selectedAnswer,
      is_correct: response.data.is_correct,
      disciplina: question.disciplina
    }])
  }

  const nextQuestion = () => {
    if (currentQuestion + 1 >= simulado.questions.length) {
      // Última questão - mostrar resultado
      setShowResult(true)
    } else {
      setCurrentQuestion(currentQuestion + 1)
      setSelectedAnswer(null)
      setFeedback(null)
    }
  }

  if (!simulado) return <div>Carregando...</div>

  // Mostrar resultado final
  if (showResult) {
    const totalQuestions = answers.length
    const correctAnswers = answers.filter(a => a.is_correct).length
    const wrongAnswers = totalQuestions - correctAnswers
    const score = ((correctAnswers / totalQuestions) * 100).toFixed(1)
    
    // Acertos por disciplina
    const byDiscipline = {}
    answers.forEach(a => {
      if (!byDiscipline[a.disciplina]) {
        byDiscipline[a.disciplina] = { total: 0, correct: 0 }
      }
      byDiscipline[a.disciplina].total++
      if (a.is_correct) byDiscipline[a.disciplina].correct++
    })

    return (
      <div className="card" style={{ maxWidth: '800px', margin: '2rem auto' }}>
        <h2 style={{ textAlign: 'center', color: '#667eea', marginBottom: '2rem' }}>
          🎉 Simulado Finalizado!
        </h2>
        
        <div style={{
          background: score >= 70 ? '#d4edda' : '#f8d7da',
          padding: '2rem',
          borderRadius: '8px',
          marginBottom: '2rem',
          textAlign: 'center'
        }}>
          <h1 style={{ fontSize: '3rem', margin: '0' }}>{score}%</h1>
          <p style={{ fontSize: '1.2rem', margin: '0.5rem 0 0 0' }}>
            {score >= 70 ? '✅ Aprovado!' : '❌ Reprovado'}
          </p>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '1rem',
          marginBottom: '2rem'
        }}>
          <div style={{ textAlign: 'center', padding: '1rem', background: '#f0f0f0', borderRadius: '8px' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{totalQuestions}</div>
            <div>Total</div>
          </div>
          <div style={{ textAlign: 'center', padding: '1rem', background: '#d4edda', borderRadius: '8px' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#28a745' }}>{correctAnswers}</div>
            <div>Acertos</div>
          </div>
          <div style={{ textAlign: 'center', padding: '1rem', background: '#f8d7da', borderRadius: '8px' }}>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#dc3545' }}>{wrongAnswers}</div>
            <div>Erros</div>
          </div>
        </div>

        <h3 style={{ marginBottom: '1rem' }}>📊 Desempenho por Disciplina</h3>
        <div style={{ marginBottom: '2rem' }}>
          {Object.entries(byDiscipline).map(([disc, stats]) => {
            const percent = ((stats.correct / stats.total) * 100).toFixed(0)
            return (
              <div key={disc} style={{ marginBottom: '1rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.25rem' }}>
                  <span>{disc}</span>
                  <span>{stats.correct}/{stats.total} ({percent}%)</span>
                </div>
                <div style={{ 
                  width: '100%', 
                  height: '8px', 
                  background: '#e0e0e0', 
                  borderRadius: '4px',
                  overflow: 'hidden'
                }}>
                  <div style={{
                    width: `${percent}%`,
                    height: '100%',
                    background: percent >= 70 ? '#28a745' : '#dc3545',
                    transition: 'width 0.3s'
                  }}></div>
                </div>
              </div>
            )
          })}
        </div>

        <button
          className="btn btn-primary"
          onClick={() => window.location.href = '/simulados'}
          style={{ width: '100%' }}
        >
          Voltar para Simulados
        </button>
      </div>
    )
  }

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
              {currentQuestion + 1 >= simulado.questions.length ? 'Ver Resultado' : 'Próxima Questão'}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

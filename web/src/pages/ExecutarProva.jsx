import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function ExecutarProva() {
  const navigate = useNavigate()
  const [prova, setProva] = useState(null)
  const [questaoAtual, setQuestaoAtual] = useState(0)
  const [respostas, setRespostas] = useState({})
  const [tempoRestante, setTempoRestante] = useState(null)
  const [mostrarResultado, setMostrarResultado] = useState(false)
  const [marcadas, setMarcadas] = useState(new Set())

  useEffect(() => {
    const provaData = localStorage.getItem('prova_atual')
    if (!provaData) {
      navigate('/prova-completa')
      return
    }
    
    const provaObj = JSON.parse(provaData)
    setProva(provaObj)
    
    // Tempo padrão: 1.5 minutos por questão
    const tempoTotal = provaObj.total_questoes * 90 // 90 segundos por questão
    setTempoRestante(tempoTotal)
  }, [navigate])

  // Timer
  useEffect(() => {
    if (tempoRestante === null || tempoRestante <= 0 || mostrarResultado) return
    
    const timer = setInterval(() => {
      setTempoRestante(prev => {
        if (prev <= 1) {
          finalizarProva()
          return 0
        }
        return prev - 1
      })
    }, 1000)
    
    return () => clearInterval(timer)
  }, [tempoRestante, mostrarResultado])

  const formatarTempo = (segundos) => {
    const horas = Math.floor(segundos / 3600)
    const minutos = Math.floor((segundos % 3600) / 60)
    const segs = segundos % 60
    return `${horas.toString().padStart(2, '0')}:${minutos.toString().padStart(2, '0')}:${segs.toString().padStart(2, '0')}`
  }

  const selecionarResposta = (alternativa) => {
    setRespostas({
      ...respostas,
      [prova.questoes[questaoAtual].id]: alternativa
    })
  }

  const marcarQuestao = () => {
    const novasMarcadas = new Set(marcadas)
    if (marcadas.has(questaoAtual)) {
      novasMarcadas.delete(questaoAtual)
    } else {
      novasMarcadas.add(questaoAtual)
    }
    setMarcadas(novasMarcadas)
  }

  const finalizarProva = () => {
    setMostrarResultado(true)
    // Salvar resultado no localStorage
    const resultado = {
      prova: prova.template,
      total_questoes: prova.total_questoes,
      respondidas: Object.keys(respostas).length,
      data: new Date().toISOString()
    }
    localStorage.setItem('ultimo_resultado', JSON.stringify(resultado))
  }

  if (!prova) {
    return <div style={{ padding: '2rem', textAlign: 'center' }}>Carregando prova...</div>
  }

  if (mostrarResultado) {
    const respondidas = Object.keys(respostas).length
    const percentual = ((respondidas / prova.total_questoes) * 100).toFixed(1)
    
    return (
      <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
        <div style={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          padding: '3rem',
          borderRadius: '12px',
          color: 'white',
          textAlign: 'center',
          marginBottom: '2rem'
        }}>
          <h1 style={{ margin: '0 0 1rem 0', fontSize: '2.5rem' }}>🎉 Prova Finalizada!</h1>
          <p style={{ fontSize: '1.2rem', opacity: 0.9 }}>Parabéns por completar o simulado!</p>
        </div>

        <div style={{
          background: 'white',
          padding: '2rem',
          borderRadius: '12px',
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          marginBottom: '2rem'
        }}>
          <h2 style={{ marginBottom: '1.5rem' }}>📊 Estatísticas</h2>
          
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: '#f7fafc', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#667eea' }}>
                {respondidas}/{prova.total_questoes}
              </div>
              <div style={{ color: '#718096' }}>Questões Respondidas</div>
            </div>
            
            <div style={{ padding: '1rem', background: '#f7fafc', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f5576c' }}>
                {percentual}%
              </div>
              <div style={{ color: '#718096' }}>Taxa de Conclusão</div>
            </div>
            
            <div style={{ padding: '1rem', background: '#f7fafc', borderRadius: '8px', textAlign: 'center' }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#43e97b' }}>
                {marcadas.size}
              </div>
              <div style={{ color: '#718096' }}>Questões Marcadas</div>
            </div>
          </div>

          <div style={{ marginTop: '2rem', padding: '1rem', background: '#fff5f5', borderRadius: '8px', border: '2px solid #feb2b2' }}>
            <p style={{ margin: 0, color: '#c53030' }}>
              <strong>⚠️ Atenção:</strong> Este é um simulado de prática. Para ver gabaritos e explicações, 
              acesse a seção de questões individuais no menu principal.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '1rem' }}>
          <button
            onClick={() => navigate('/prova-completa')}
            style={{
              flex: 1,
              padding: '1rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1rem',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            🔄 Nova Prova
          </button>
          
          <button
            onClick={() => navigate('/dashboard')}
            style={{
              flex: 1,
              padding: '1rem',
              background: '#48bb78',
              color: 'white',
              border: 'none',
              borderRadius: '8px',
              fontSize: '1rem',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
          >
            🏠 Voltar ao Início
          </button>
        </div>
      </div>
    )
  }

  const questao = prova.questoes[questaoAtual]
  const alternativas = ['A', 'B', 'C', 'D']

  return (
    <div style={{ minHeight: '100vh', background: '#f7fafc' }}>
      {/* Header fixo */}
      <div style={{
        position: 'sticky',
        top: 0,
        background: 'white',
        boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        zIndex: 100,
        padding: '1rem 2rem'
      }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.2rem' }}>{prova.template}</h2>
            <p style={{ margin: '0.25rem 0 0 0', color: '#718096', fontSize: '0.9rem' }}>
              Questão {questaoAtual + 1} de {prova.total_questoes}
            </p>
          </div>
          
          <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '0.8rem', color: '#718096' }}>Tempo Restante</div>
              <div style={{
                fontSize: '1.5rem',
                fontWeight: 'bold',
                color: tempoRestante < 300 ? '#f5576c' : '#667eea'
              }}>
                {formatarTempo(tempoRestante)}
              </div>
            </div>
            
            <button
              onClick={finalizarProva}
              style={{
                padding: '0.75rem 1.5rem',
                background: '#f5576c',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontWeight: 'bold',
                cursor: 'pointer'
              }}
            >
              Finalizar Prova
            </button>
          </div>
        </div>
      </div>

      <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', display: 'flex', gap: '2rem' }}>
        {/* Questão */}
        <div style={{ flex: 1 }}>
          <div style={{
            background: 'white',
            padding: '2rem',
            borderRadius: '12px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            marginBottom: '1.5rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
              <span style={{
                padding: '0.5rem 1rem',
                background: '#667eea',
                color: 'white',
                borderRadius: '6px',
                fontSize: '0.9rem',
                fontWeight: 'bold'
              }}>
                {questao.disciplina}
              </span>
              
              <button
                onClick={marcarQuestao}
                style={{
                  padding: '0.5rem 1rem',
                  background: marcadas.has(questaoAtual) ? '#f5576c' : '#e2e8f0',
                  color: marcadas.has(questaoAtual) ? 'white' : '#4a5568',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: 'bold'
                }}
              >
                {marcadas.has(questaoAtual) ? '🚩 Marcada' : '🏳️ Marcar'}
              </button>
            </div>
            
            <h3 style={{ fontSize: '1.1rem', lineHeight: '1.6', marginBottom: '1.5rem' }}>
              {questao.enunciado}
            </h3>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {alternativas.map((letra) => {
                const textoAlternativa = questao[`alternativa_${letra.toLowerCase()}`]
                const selecionada = respostas[questao.id] === letra
                
                return (
                  <div
                    key={letra}
                    onClick={() => selecionarResposta(letra)}
                    style={{
                      padding: '1rem',
                      background: selecionada ? '#e6fffa' : '#f7fafc',
                      border: selecionada ? '3px solid #38b2ac' : '2px solid #e2e8f0',
                      borderRadius: '8px',
                      cursor: 'pointer',
                      transition: 'all 0.2s ease',
                      display: 'flex',
                      gap: '1rem'
                    }}
                  >
                    <div style={{
                      width: '32px',
                      height: '32px',
                      borderRadius: '50%',
                      background: selecionada ? '#38b2ac' : '#e2e8f0',
                      color: selecionada ? 'white' : '#4a5568',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 'bold',
                      flexShrink: 0
                    }}>
                      {letra}
                    </div>
                    <div style={{ flex: 1, paddingTop: '0.25rem' }}>{textoAlternativa}</div>
                  </div>
                )
              })}
            </div>
          </div>

          {/* Navegação */}
          <div style={{ display: 'flex', gap: '1rem' }}>
            <button
              onClick={() => setQuestaoAtual(Math.max(0, questaoAtual - 1))}
              disabled={questaoAtual === 0}
              style={{
                flex: 1,
                padding: '1rem',
                background: questaoAtual === 0 ? '#e2e8f0' : '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontWeight: 'bold',
                cursor: questaoAtual === 0 ? 'not-allowed' : 'pointer'
              }}
            >
              ← Anterior
            </button>
            
            <button
              onClick={() => setQuestaoAtual(Math.min(prova.questoes.length - 1, questaoAtual + 1))}
              disabled={questaoAtual === prova.questoes.length - 1}
              style={{
                flex: 1,
                padding: '1rem',
                background: questaoAtual === prova.questoes.length - 1 ? '#e2e8f0' : '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '8px',
                fontWeight: 'bold',
                cursor: questaoAtual === prova.questoes.length - 1 ? 'not-allowed' : 'pointer'
              }}
            >
              Próxima →
            </button>
          </div>
        </div>

        {/* Mapa de questões */}
        <div style={{ width: '300px' }}>
          <div style={{
            background: 'white',
            padding: '1.5rem',
            borderRadius: '12px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
            position: 'sticky',
            top: '100px'
          }}>
            <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.1rem' }}>Mapa de Questões</h3>
            
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(5, 1fr)',
              gap: '0.5rem',
              marginBottom: '1rem'
            }}>
              {prova.questoes.map((q, idx) => {
                const respondida = respostas[q.id]
                const marcada = marcadas.has(idx)
                const atual = idx === questaoAtual
                
                return (
                  <button
                    key={idx}
                    onClick={() => setQuestaoAtual(idx)}
                    style={{
                      width: '40px',
                      height: '40px',
                      border: atual ? '3px solid #667eea' : 'none',
                      borderRadius: '6px',
                      background: marcada ? '#f5576c' : respondida ? '#48bb78' : '#e2e8f0',
                      color: marcada || respondida ? 'white' : '#4a5568',
                      fontWeight: 'bold',
                      cursor: 'pointer',
                      fontSize: '0.9rem'
                    }}
                  >
                    {idx + 1}
                  </button>
                )
              })}
            </div>
            
            <div style={{ fontSize: '0.85rem', color: '#718096' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <div style={{ width: '16px', height: '16px', background: '#48bb78', borderRadius: '4px' }}></div>
                <span>Respondida</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
                <div style={{ width: '16px', height: '16px', background: '#f5576c', borderRadius: '4px' }}></div>
                <span>Marcada</span>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <div style={{ width: '16px', height: '16px', background: '#e2e8f0', borderRadius: '4px' }}></div>
                <span>Não respondida</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

import { useState, useEffect } from 'react'
import { useQuery, useMutation } from '@tanstack/react-query'
import axios from 'axios'
import { API_URL } from '../config'
import { useNavigate } from 'react-router-dom'

export default function ProvaCompleta() {
  const navigate = useNavigate()
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [showStats, setShowStats] = useState(false)

  // Buscar templates disponíveis
  const { data: templates } = useQuery({
    queryKey: ['templates-provas'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/templates-provas`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.templates
    }
  })

  // Buscar estatísticas do banco
  const { data: stats } = useQuery({
    queryKey: ['estatisticas-banco'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/estatisticas-banco`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    }
  })

  // Gerar prova completa
  const gerarProva = useMutation({
    mutationFn: async (templateId) => {
      const token = localStorage.getItem('token')
      const response = await axios.post(
        `${API_URL}/api/gerar-prova-completa?template_id=${templateId}`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      return response.data
    },
    onSuccess: (data) => {
      // Salvar prova no localStorage e navegar para execução
      localStorage.setItem('prova_atual', JSON.stringify(data))
      navigate('/executar-prova')
    },
    onError: (error) => {
      alert('Erro ao gerar prova: ' + (error.response?.data?.detail || error.message))
    }
  })

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '2rem',
        borderRadius: '12px',
        color: 'white',
        marginBottom: '2rem',
        boxShadow: '0 10px 30px rgba(0,0,0,0.2)'
      }}>
        <h1 style={{ margin: 0, fontSize: '2rem', fontWeight: 'bold' }}>
          🎯 Prova Completa - Câmara de Porto Velho
        </h1>
        <p style={{ margin: '0.5rem 0 0 0', opacity: 0.9 }}>
          Técnico em Informática - Sistema de Preparação Completo
        </p>
      </div>

      {/* Estatísticas do Banco */}
      {stats && (
        <div style={{
          background: 'white',
          padding: '1.5rem',
          borderRadius: '12px',
          marginBottom: '2rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <h2 style={{ margin: 0, fontSize: '1.3rem' }}>📊 Banco de Questões</h2>
            <button
              onClick={() => setShowStats(!showStats)}
              style={{
                padding: '0.5rem 1rem',
                background: '#667eea',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer'
              }}
            >
              {showStats ? 'Ocultar' : 'Ver Detalhes'}
            </button>
          </div>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '1rem'
          }}>
            <div style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              padding: '1rem',
              borderRadius: '8px',
              color: 'white',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>{stats.total_questoes}</div>
              <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Total de Questões</div>
            </div>
            
            <div style={{
              background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              padding: '1rem',
              borderRadius: '8px',
              color: 'white',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                {stats.por_disciplina?.Informática || 0}
              </div>
              <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Informática</div>
            </div>
            
            <div style={{
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              padding: '1rem',
              borderRadius: '8px',
              color: 'white',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                {stats.por_disciplina?.Português || 0}
              </div>
              <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Português</div>
            </div>
            
            <div style={{
              background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
              padding: '1rem',
              borderRadius: '8px',
              color: 'white',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '2rem', fontWeight: 'bold' }}>
                {stats.por_disciplina?.Matemática || 0}
              </div>
              <div style={{ fontSize: '0.9rem', opacity: 0.9 }}>Matemática</div>
            </div>
          </div>

          {showStats && stats.por_disciplina && (
            <div style={{ marginTop: '1rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px' }}>
              <h3 style={{ margin: '0 0 1rem 0', fontSize: '1rem' }}>Detalhamento por Disciplina:</h3>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '0.5rem' }}>
                {Object.entries(stats.por_disciplina).map(([disc, count]) => (
                  <div key={disc} style={{ display: 'flex', justifyContent: 'space-between', padding: '0.5rem' }}>
                    <span style={{ fontWeight: '500' }}>{disc}:</span>
                    <span style={{ color: '#667eea', fontWeight: 'bold' }}>{count} questões</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Templates de Prova */}
      <div>
        <h2 style={{ marginBottom: '1.5rem', fontSize: '1.5rem' }}>📝 Escolha o Tipo de Prova</h2>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '1.5rem'
        }}>
          {templates?.map((template) => (
            <div
              key={template.id}
              style={{
                background: 'white',
                padding: '1.5rem',
                borderRadius: '12px',
                boxShadow: selectedTemplate === template.id 
                  ? '0 8px 24px rgba(102, 126, 234, 0.4)' 
                  : '0 2px 8px rgba(0,0,0,0.1)',
                border: selectedTemplate === template.id ? '3px solid #667eea' : '3px solid transparent',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                transform: selectedTemplate === template.id ? 'translateY(-4px)' : 'none'
              }}
              onClick={() => setSelectedTemplate(template.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
                <h3 style={{ margin: 0, fontSize: '1.2rem', color: '#2d3748' }}>
                  {template.nome}
                </h3>
                {selectedTemplate === template.id && (
                  <span style={{ fontSize: '1.5rem' }}>✅</span>
                )}
              </div>
              
              <p style={{ color: '#718096', fontSize: '0.9rem', marginBottom: '1rem' }}>
                {template.descricao}
              </p>
              
              <div style={{
                background: '#f7fafc',
                padding: '1rem',
                borderRadius: '8px',
                marginBottom: '1rem'
              }}>
                <div style={{ fontWeight: 'bold', marginBottom: '0.5rem', color: '#667eea' }}>
                  📊 {template.total_questoes} questões
                </div>
                <div style={{ fontSize: '0.85rem', color: '#4a5568' }}>
                  {template.disciplinas.map((disc, idx) => (
                    <span key={disc}>
                      {disc}
                      {idx < template.disciplinas.length - 1 ? ' • ' : ''}
                    </span>
                  ))}
                </div>
              </div>
              
              <button
                onClick={(e) => {
                  e.stopPropagation()
                  gerarProva.mutate(template.id)
                }}
                disabled={gerarProva.isPending}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  background: gerarProva.isPending 
                    ? '#cbd5e0' 
                    : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  color: 'white',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '1rem',
                  fontWeight: 'bold',
                  cursor: gerarProva.isPending ? 'not-allowed' : 'pointer',
                  transition: 'all 0.3s ease'
                }}
              >
                {gerarProva.isPending ? '⏳ Gerando...' : '🚀 Iniciar Prova'}
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Dicas de Estudo */}
      <div style={{
        marginTop: '3rem',
        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        padding: '2rem',
        borderRadius: '12px',
        color: 'white'
      }}>
        <h2 style={{ margin: '0 0 1rem 0', fontSize: '1.5rem' }}>💡 Dicas para sua Preparação</h2>
        <ul style={{ margin: 0, paddingLeft: '1.5rem', lineHeight: '1.8' }}>
          <li><strong>Foco em Informática:</strong> 50% da prova é conhecimento específico</li>
          <li><strong>Não negligencie Português:</strong> Interpretação de texto é fundamental</li>
          <li><strong>Pratique Raciocínio Lógico:</strong> Questões de lógica aparecem em todas as provas</li>
          <li><strong>Estude Legislação de RO:</strong> Conhecer leis locais faz diferença</li>
          <li><strong>Faça simulados regularmente:</strong> A prática leva à perfeição</li>
        </ul>
      </div>
    </div>
  )
}

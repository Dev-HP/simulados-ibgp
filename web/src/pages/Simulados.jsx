import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Link } from 'react-router-dom'
import axios from 'axios'
import { API_URL } from '../config'

export default function Simulados() {
  const [showCreate, setShowCreate] = useState(false)
  const [selectedTopics, setSelectedTopics] = useState([])
  const [selectedDisciplinas, setSelectedDisciplinas] = useState([])
  const [formData, setFormData] = useState({
    nome: '',
    numero_questoes: 20,
    tempo_total: 60,
    dificuldade: 'MEDIO'
  })

  // Buscar tópicos disponíveis
  const { data: topics } = useQuery({
    queryKey: ['topics'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/topics`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    }
  })

  // Buscar simulados existentes
  const { data: simulados, refetch } = useQuery({
    queryKey: ['simulados'],
    queryFn: async () => {
      const token = localStorage.getItem('token')
      const response = await axios.get(`${API_URL}/api/simulados`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    }
  })

  // Agrupar tópicos por disciplina
  const disciplinas = topics ? [...new Set(topics.map(t => t.disciplina))] : []
  
  const toggleDisciplina = (disciplina) => {
    if (selectedDisciplinas.includes(disciplina)) {
      setSelectedDisciplinas(selectedDisciplinas.filter(d => d !== disciplina))
      // Remove todos os tópicos dessa disciplina
      const topicsToRemove = topics.filter(t => t.disciplina === disciplina).map(t => t.id)
      setSelectedTopics(selectedTopics.filter(id => !topicsToRemove.includes(id)))
    } else {
      setSelectedDisciplinas([...selectedDisciplinas, disciplina])
      // Adiciona todos os tópicos dessa disciplina
      const topicsToAdd = topics.filter(t => t.disciplina === disciplina).map(t => t.id)
      setSelectedTopics([...new Set([...selectedTopics, ...topicsToAdd])])
    }
  }

  const toggleTopic = (topicId) => {
    if (selectedTopics.includes(topicId)) {
      setSelectedTopics(selectedTopics.filter(id => id !== topicId))
    } else {
      setSelectedTopics([...selectedTopics, topicId])
    }
  }

  const handleCreate = async () => {
    try {
      const token = localStorage.getItem('token')
      
      const payload = {
        ...formData,
        topic_ids: selectedTopics.length > 0 ? selectedTopics : undefined
      }
      
      await axios.post(`${API_URL}/api/create-simulado`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      })
      
      setShowCreate(false)
      setSelectedTopics([])
      setSelectedDisciplinas([])
      setFormData({
        nome: '',
        numero_questoes: 20,
        tempo_total: 60,
        dificuldade: 'MEDIO'
      })
      refetch()
      alert('Simulado criado com sucesso!')
    } catch (error) {
      alert('Erro ao criar simulado: ' + (error.response?.data?.detail || error.message))
    }
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ 
        background: 'white', 
        padding: '2rem', 
        borderRadius: '8px', 
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
        marginBottom: '2rem'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ margin: 0 }}>Simulados Personalizados</h1>
          <button 
            style={{
              padding: '0.75rem 1.5rem',
              background: '#4CAF50',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '1rem',
              fontWeight: 'bold'
            }}
            onClick={() => setShowCreate(!showCreate)}
          >
            {showCreate ? 'Cancelar' : '+ Criar Simulado'}
          </button>
        </div>
      </div>

      {showCreate && (
        <div style={{ 
          background: 'white', 
          padding: '2rem', 
          borderRadius: '8px', 
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
          marginBottom: '2rem'
        }}>
          <h2>Novo Simulado Personalizado</h2>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem', marginTop: '1.5rem' }}>
            {/* Nome */}
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Nome do Simulado:
              </label>
              <input
                type="text"
                placeholder="Ex: Simulado de Informática"
                value={formData.nome}
                onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '1rem'
                }}
              />
            </div>

            {/* Número de questões */}
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Número de Questões:
              </label>
              <input
                type="number"
                min="5"
                max="100"
                value={formData.numero_questoes}
                onChange={(e) => setFormData({ ...formData, numero_questoes: parseInt(e.target.value) })}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '1rem'
                }}
              />
            </div>

            {/* Tempo */}
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Tempo Total (minutos):
              </label>
              <input
                type="number"
                min="10"
                max="240"
                value={formData.tempo_total}
                onChange={(e) => setFormData({ ...formData, tempo_total: parseInt(e.target.value) })}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '1rem'
                }}
              />
            </div>

            {/* Dificuldade */}
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Dificuldade:
              </label>
              <select
                value={formData.dificuldade}
                onChange={(e) => setFormData({ ...formData, dificuldade: e.target.value })}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  fontSize: '1rem'
                }}
              >
                <option value="FACIL">Fácil</option>
                <option value="MEDIO">Médio</option>
                <option value="DIFICIL">Difícil</option>
                <option value="MISTO">Misto (todas)</option>
              </select>
            </div>

            {/* Seleção de Disciplinas */}
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Disciplinas (opcional - deixe vazio para todas):
              </label>
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', 
                gap: '0.5rem',
                marginTop: '0.5rem'
              }}>
                {disciplinas.map(disc => (
                  <label 
                    key={disc}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      padding: '0.5rem',
                      background: selectedDisciplinas.includes(disc) ? '#e3f2fd' : '#f5f5f5',
                      borderRadius: '4px',
                      cursor: 'pointer',
                      border: selectedDisciplinas.includes(disc) ? '2px solid #2196F3' : '2px solid transparent'
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={selectedDisciplinas.includes(disc)}
                      onChange={() => toggleDisciplina(disc)}
                      style={{ marginRight: '0.5rem' }}
                    />
                    <span style={{ fontSize: '0.9rem' }}>{disc}</span>
                  </label>
                ))}
              </div>
            </div>

            {/* Seleção de Tópicos Específicos */}
            {selectedDisciplinas.length > 0 && (
              <div>
                <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                  Tópicos Específicos (opcional):
                </label>
                <div style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #ddd', borderRadius: '4px', padding: '1rem' }}>
                  {selectedDisciplinas.map(disc => (
                    <div key={disc} style={{ marginBottom: '1rem' }}>
                      <h4 style={{ margin: '0 0 0.5rem 0', color: '#2196F3' }}>{disc}</h4>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.25rem' }}>
                        {topics
                          .filter(t => t.disciplina === disc)
                          .map(topic => (
                            <label 
                              key={topic.id}
                              style={{
                                display: 'flex',
                                alignItems: 'center',
                                padding: '0.25rem',
                                cursor: 'pointer'
                              }}
                            >
                              <input
                                type="checkbox"
                                checked={selectedTopics.includes(topic.id)}
                                onChange={() => toggleTopic(topic.id)}
                                style={{ marginRight: '0.5rem' }}
                              />
                              <span style={{ fontSize: '0.85rem' }}>
                                {topic.topico} {topic.subtopico && `- ${topic.subtopico}`}
                              </span>
                            </label>
                          ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Resumo */}
            <div style={{ 
              background: '#f5f5f5', 
              padding: '1rem', 
              borderRadius: '4px',
              border: '1px solid #ddd'
            }}>
              <h4 style={{ margin: '0 0 0.5rem 0' }}>Resumo:</h4>
              <p style={{ margin: '0.25rem 0' }}>
                📝 {formData.numero_questoes} questões
              </p>
              <p style={{ margin: '0.25rem 0' }}>
                ⏱️ {formData.tempo_total} minutos
              </p>
              <p style={{ margin: '0.25rem 0' }}>
                📊 Dificuldade: {formData.dificuldade}
              </p>
              <p style={{ margin: '0.25rem 0' }}>
                📚 {selectedDisciplinas.length > 0 
                  ? `${selectedDisciplinas.length} disciplina(s) selecionada(s)` 
                  : 'Todas as disciplinas'}
              </p>
              <p style={{ margin: '0.25rem 0' }}>
                🎯 {selectedTopics.length > 0 
                  ? `${selectedTopics.length} tópico(s) específico(s)` 
                  : 'Todos os tópicos'}
              </p>
            </div>

            {/* Botão Criar */}
            <button 
              onClick={handleCreate}
              disabled={!formData.nome}
              style={{
                padding: '1rem',
                background: formData.nome ? '#4CAF50' : '#ccc',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: formData.nome ? 'pointer' : 'not-allowed',
                fontSize: '1.1rem',
                fontWeight: 'bold'
              }}
            >
              ✅ Criar Simulado
            </button>
          </div>
        </div>
      )}

      {/* Lista de Simulados */}
      <div style={{ display: 'grid', gap: '1rem' }}>
        {simulados?.map((sim) => (
          <div 
            key={sim.id} 
            style={{ 
              background: 'white', 
              padding: '1.5rem', 
              borderRadius: '8px', 
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center'
            }}
          >
            <div>
              <h3 style={{ margin: '0 0 0.5rem 0' }}>{sim.nome}</h3>
              <p style={{ margin: 0, color: '#666' }}>
                {sim.numero_questoes} questões • {sim.tempo_total} minutos
              </p>
            </div>
            <Link to={`/simulados/${sim.id}`}>
              <button style={{
                padding: '0.75rem 1.5rem',
                background: '#2196F3',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '1rem',
                fontWeight: 'bold'
              }}>
                Iniciar →
              </button>
            </Link>
          </div>
        ))}
        
        {(!simulados || simulados.length === 0) && !showCreate && (
          <div style={{ 
            background: 'white', 
            padding: '3rem', 
            borderRadius: '8px', 
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            textAlign: 'center'
          }}>
            <p style={{ fontSize: '1.2rem', color: '#666' }}>
              Nenhum simulado criado ainda.
            </p>
            <p style={{ color: '#999' }}>
              Clique em "Criar Simulado" para começar!
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

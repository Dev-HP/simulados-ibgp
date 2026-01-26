import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

export default function Simulados() {
  const [showCreate, setShowCreate] = useState(false)
  const [formData, setFormData] = useState({
    nome: '',
    numero_questoes: 20,
    tempo_total: 60
  })

  const { data: simulados, refetch } = useQuery({
    queryKey: ['simulados'],
    queryFn: async () => {
      const response = await axios.get('/api/simulados')
      return response.data
    }
  })

  const handleCreate = async () => {
    try {
      await axios.post('/api/create-simulado', formData)
      setShowCreate(false)
      refetch()
    } catch (error) {
      alert('Erro ao criar simulado: ' + error.message)
    }
  }

  return (
    <div>
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1>Simulados</h1>
          <button className="btn btn-primary" onClick={() => setShowCreate(!showCreate)}>
            Criar Simulado
          </button>
        </div>
      </div>

      {showCreate && (
        <div className="card">
          <h2>Novo Simulado</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <input
              type="text"
              placeholder="Nome do simulado"
              value={formData.nome}
              onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
            />
            <input
              type="number"
              placeholder="Número de questões"
              value={formData.numero_questoes}
              onChange={(e) => setFormData({ ...formData, numero_questoes: parseInt(e.target.value) })}
            />
            <input
              type="number"
              placeholder="Tempo total (minutos)"
              value={formData.tempo_total}
              onChange={(e) => setFormData({ ...formData, tempo_total: parseInt(e.target.value) })}
            />
            <button className="btn btn-success" onClick={handleCreate}>
              Criar
            </button>
          </div>
        </div>
      )}

      <div>
        {simulados?.map((sim) => (
          <div key={sim.id} className="card">
            <h3>{sim.nome}</h3>
            <p>{sim.numero_questoes} questões • {sim.tempo_total} minutos</p>
            <a href={`/simulados/${sim.id}`}>
              <button className="btn btn-primary">Iniciar</button>
            </a>
          </div>
        ))}
      </div>
    </div>
  )
}

import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { API_URL } from '../config'

export default function AIGenerator() {
  const [activeTab, setActiveTab] = useState('import')
  const [importFile, setImportFile] = useState(null)
  const [importDisciplina, setImportDisciplina] = useState('Informática')
  const [importLoading, setImportLoading] = useState(false)
  const [importMessage, setImportMessage] = useState('')
  
  const [selectedTopic, setSelectedTopic] = useState('')
  const [quantity, setQuantity] = useState(10)
  const [difficulty, setDifficulty] = useState('MEDIO')
  const [useReferences, setUseReferences] = useState(true)
  const [generateLoading, setGenerateLoading] = useState(false)
  const [generateMessage, setGenerateMessage] = useState('')

  // Buscar tópicos disponíveis
  const { data: topics } = useQuery({
    queryKey: ['topics'],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/api/topics`)
      return response.data
    }
  })

  // Buscar estatísticas
  const { data: stats } = useQuery({
    queryKey: ['question-stats'],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/api/questions?limit=1000`)
      const questions = response.data
      return {
        total: questions.length,
        byDisciplina: questions.reduce((acc, q) => {
          acc[q.disciplina] = (acc[q.disciplina] || 0) + 1
          return acc
        }, {}),
        byDifficulty: questions.reduce((acc, q) => {
          acc[q.dificuldade] = (acc[q.dificuldade] || 0) + 1
          return acc
        }, {})
      }
    }
  })

  const handleImport = async () => {
    if (!importFile) return

    setImportLoading(true)
    setImportMessage('')

    const formData = new FormData()
    formData.append('file', importFile)
    formData.append('disciplina', importDisciplina)

    try {
      const response = await axios.post(`${API_URL}/api/import-questions`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      
      setImportMessage(`✅ ${response.data.total_imported} questões importadas com sucesso!`)
      setImportFile(null)
      
      // Atualizar estatísticas
      setTimeout(() => window.location.reload(), 2000)
    } catch (error) {
      setImportMessage(`❌ Erro: ${error.response?.data?.detail || error.message}`)
    } finally {
      setImportLoading(false)
    }
  }

  const handleGenerate = async () => {
    if (!selectedTopic) {
      setGenerateMessage('❌ Selecione um tópico')
      return
    }

    setGenerateLoading(true)
    setGenerateMessage('')

    try {
      const response = await axios.post(`${API_URL}/api/generate-with-ai`, null, {
        params: {
          topic_id: selectedTopic,
          quantity: quantity,
          difficulty: difficulty,
          use_references: useReferences
        }
      })
      
      setGenerateMessage(`✅ ${response.data.total_generated} questões geradas com IA!`)
      
      // Atualizar estatísticas
      setTimeout(() => window.location.reload(), 2000)
    } catch (error) {
      const errorMsg = error.response?.data?.detail || error.message
      if (errorMsg.includes('GEMINI_API_KEY')) {
        setGenerateMessage('❌ Chave do Gemini não configurada. Configure no Render.')
      } else {
        setGenerateMessage(`❌ Erro: ${errorMsg}`)
      }
    } finally {
      setGenerateLoading(false)
    }
  }

  return (
    <div>
      <div className="card">
        <h1>🤖 Gerador de Questões com IA</h1>
        <p>Importe questões reais e gere novas questões usando Gemini AI</p>
      </div>

      {/* Estatísticas */}
      {stats && (
        <div className="card">
          <h2>📊 Estatísticas do Banco</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: '#e3f2fd', borderRadius: '8px' }}>
              <h3 style={{ margin: 0, fontSize: '2rem' }}>{stats.total}</h3>
              <p style={{ margin: '0.5rem 0 0 0', color: '#666' }}>Total de Questões</p>
            </div>
            
            {Object.entries(stats.byDisciplina).map(([disc, count]) => (
              <div key={disc} style={{ padding: '1rem', background: '#f3e5f5', borderRadius: '8px' }}>
                <h3 style={{ margin: 0, fontSize: '1.5rem' }}>{count}</h3>
                <p style={{ margin: '0.5rem 0 0 0', color: '#666' }}>{disc}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="card">
        <div style={{ display: 'flex', gap: '1rem', borderBottom: '2px solid #eee', marginBottom: '2rem' }}>
          <button
            onClick={() => setActiveTab('import')}
            style={{
              padding: '1rem 2rem',
              border: 'none',
              background: 'none',
              borderBottom: activeTab === 'import' ? '3px solid #007bff' : 'none',
              color: activeTab === 'import' ? '#007bff' : '#666',
              fontWeight: activeTab === 'import' ? 'bold' : 'normal',
              cursor: 'pointer'
            }}
          >
            📥 Importar Questões Reais
          </button>
          <button
            onClick={() => setActiveTab('generate')}
            style={{
              padding: '1rem 2rem',
              border: 'none',
              background: 'none',
              borderBottom: activeTab === 'generate' ? '3px solid #007bff' : 'none',
              color: activeTab === 'generate' ? '#007bff' : '#666',
              fontWeight: activeTab === 'generate' ? 'bold' : 'normal',
              cursor: 'pointer'
            }}
          >
            🤖 Gerar com IA
          </button>
        </div>

        {/* Tab: Importar */}
        {activeTab === 'import' && (
          <div>
            <h2>Importar Questões de Provas Reais</h2>
            <p style={{ color: '#666', marginBottom: '2rem' }}>
              Faça upload de PDFs ou arquivos TXT com questões de provas anteriores.
              Essas questões servirão como referência para a IA gerar novas questões.
            </p>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Arquivo da Prova (PDF ou TXT)
              </label>
              <input
                type="file"
                accept=".pdf,.txt"
                onChange={(e) => setImportFile(e.target.files[0])}
                style={{ padding: '0.5rem' }}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Disciplina
              </label>
              <select
                value={importDisciplina}
                onChange={(e) => setImportDisciplina(e.target.value)}
                style={{ width: '100%', padding: '0.5rem' }}
              >
                <option value="Informática">Informática</option>
                <option value="Hardware">Hardware</option>
                <option value="Redes">Redes</option>
                <option value="Linux">Linux</option>
                <option value="Windows">Windows</option>
                <option value="Banco de Dados">Banco de Dados</option>
                <option value="Segurança">Segurança</option>
                <option value="Programação">Programação</option>
              </select>
            </div>

            <button
              className="btn btn-primary"
              onClick={handleImport}
              disabled={!importFile || importLoading}
              style={{ width: '100%' }}
            >
              {importLoading ? '⏳ Importando...' : '📥 Importar Questões'}
            </button>

            {importMessage && (
              <div style={{
                marginTop: '1rem',
                padding: '1rem',
                background: importMessage.includes('✅') ? '#d4edda' : '#f8d7da',
                borderRadius: '4px'
              }}>
                {importMessage}
              </div>
            )}

            <div style={{ marginTop: '2rem', padding: '1rem', background: '#fff3cd', borderRadius: '4px' }}>
              <strong>📝 Formato esperado:</strong>
              <pre style={{ marginTop: '0.5rem', fontSize: '0.9rem' }}>
{`QUESTÃO 1
Sobre hardware, é correto afirmar que:
A) RAM é memória volátil
B) ROM é memória volátil
C) Cache é mais lenta que RAM
D) SSD é mais lento que HD
Gabarito: A

QUESTÃO 2
...`}
              </pre>
            </div>
          </div>
        )}

        {/* Tab: Gerar com IA */}
        {activeTab === 'generate' && (
          <div>
            <h2>Gerar Questões com Gemini AI</h2>
            <p style={{ color: '#666', marginBottom: '2rem' }}>
              A IA vai gerar questões novas baseadas nas questões reais importadas,
              mantendo o estilo e qualidade de concurso público.
            </p>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Tópico do Edital
              </label>
              <select
                value={selectedTopic}
                onChange={(e) => setSelectedTopic(e.target.value)}
                style={{ width: '100%', padding: '0.5rem' }}
              >
                <option value="">Selecione um tópico...</option>
                {topics?.map((topic) => (
                  <option key={topic.id} value={topic.id}>
                    {topic.disciplina} - {topic.topico}
                  </option>
                ))}
              </select>
              {!topics?.length && (
                <p style={{ color: '#dc3545', fontSize: '0.9rem', marginTop: '0.5rem' }}>
                  ⚠️ Nenhum tópico encontrado. Faça upload do edital primeiro.
                </p>
              )}
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Quantidade de Questões
              </label>
              <input
                type="number"
                min="1"
                max="50"
                value={quantity}
                onChange={(e) => setQuantity(parseInt(e.target.value))}
                style={{ width: '100%', padding: '0.5rem' }}
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', marginBottom: '0.5rem', fontWeight: 'bold' }}>
                Dificuldade
              </label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                style={{ width: '100%', padding: '0.5rem' }}
              >
                <option value="FACIL">Fácil</option>
                <option value="MEDIO">Médio</option>
                <option value="DIFICIL">Difícil</option>
              </select>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input
                  type="checkbox"
                  checked={useReferences}
                  onChange={(e) => setUseReferences(e.target.checked)}
                />
                <span>Usar questões reais como referência (recomendado)</span>
              </label>
            </div>

            <button
              className="btn btn-primary"
              onClick={handleGenerate}
              disabled={!selectedTopic || generateLoading}
              style={{ width: '100%' }}
            >
              {generateLoading ? '⏳ Gerando com IA...' : '🤖 Gerar Questões'}
            </button>

            {generateMessage && (
              <div style={{
                marginTop: '1rem',
                padding: '1rem',
                background: generateMessage.includes('✅') ? '#d4edda' : '#f8d7da',
                borderRadius: '4px'
              }}>
                {generateMessage}
              </div>
            )}

            <div style={{ marginTop: '2rem', padding: '1rem', background: '#d1ecf1', borderRadius: '4px' }}>
              <strong>💡 Dica:</strong> Importe várias provas reais antes de gerar com IA.
              Quanto mais referências, melhor a qualidade das questões geradas!
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

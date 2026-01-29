import { Link } from 'react-router-dom'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'
import { API_URL } from '../config'

export default function Dashboard() {
  // Buscar estatísticas
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

  const handleGerarProvaCompleta = async () => {
    if (!confirm('🚀 Gerar TODAS as 60 questões da prova real do concurso?\n\n⏱️ Isso pode levar 15-20 minutos.\n\n✅ Clique OK para continuar.')) {
      return
    }

    alert('🎯 Geração iniciada!\n\nO sistema vai gerar 60 questões seguindo o edital:\n• 30 Informática\n• 9 Português\n• 6 Matemática\n• 4 Raciocínio Lógico\n• 7 Legislação\n• 4 Conhecimentos Gerais\n\n⏱️ Aguarde 15-20 minutos.\n\nVocê pode fechar esta janela e voltar depois.')

    try {
      const token = localStorage.getItem('token')
      
      // Chamar endpoint especial (vamos criar)
      const response = await axios.post(
        `${API_URL}/api/gerar-prova-completa-concurso`,
        {},
        { headers: { Authorization: `Bearer ${token}` }, timeout: 1200000 }
      )
      
      if (response.status === 200) {
        alert('🎉 SUCESSO!\n\n✅ Todas as questões foram geradas!\n\n🎯 Agora você pode fazer a prova completa.')
        window.location.reload()
      }
    } catch (error) {
      alert('⚠️ Erro na geração.\n\nUse o script Python:\npython gerar_prova_completa_concurso.py')
    }
  }

  const cards = [
    {
      title: '🎯 Prova Completa',
      description: 'Simulado completo do concurso da Câmara de Porto Velho',
      link: '/prova-completa',
      gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      highlight: true
    },
    {
      title: '⚡ GERAR PROVA REAL',
      description: 'Gera TODAS as 60 questões do concurso seguindo o edital (15-20 min)',
      action: handleGerarProvaCompleta,
      gradient: 'linear-gradient(135deg, #FF6B6B 0%, #FFE66D 100%)',
      highlight: true,
      special: true
    },
    {
      title: '🧠 Aprendizado Adaptativo',
      description: 'Análise personalizada e plano de estudos inteligente',
      link: '/adaptive-learning',
      gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
      highlight: true
    },
    {
      title: '🤖 Gerar com IA',
      description: 'Crie questões personalizadas com Inteligência Artificial',
      link: '/ai-generator',
      gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'
    },
    {
      title: '📚 Questões',
      description: 'Pratique questões por disciplina e tópico',
      link: '/questions',
      gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    },
    {
      title: '📝 Simulados',
      description: 'Simulados personalizados e adaptativos',
      link: '/simulados',
      gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)'
    }
  ]

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      {/* Hero Section */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: '3rem 2rem',
        borderRadius: '16px',
        color: 'white',
        marginBottom: '3rem',
        boxShadow: '0 20px 60px rgba(102, 126, 234, 0.3)'
      }}>
        <h1 style={{ margin: 0, fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
          🚀 Sistema de Preparação
        </h1>
        <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 'normal', opacity: 0.95 }}>
          Técnico em Informática - Câmara de Porto Velho/RO
        </h2>
        <p style={{ margin: '1rem 0 0 0', fontSize: '1.1rem', opacity: 0.9 }}>
          Prepare-se com questões geradas por IA, simulados completos e estatísticas detalhadas
        </p>
      </div>

      {/* Estatísticas Rápidas */}
      {stats && (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '1.5rem',
          marginBottom: '3rem'
        }}>
          <div style={{
            background: 'white',
            padding: '1.5rem',
            borderRadius: '12px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>📊</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#667eea', marginBottom: '0.25rem' }}>
              {stats.total_questoes}
            </div>
            <div style={{ color: '#718096', fontSize: '0.95rem' }}>Total de Questões</div>
          </div>

          <div style={{
            background: 'white',
            padding: '1.5rem',
            borderRadius: '12px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>💻</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f5576c', marginBottom: '0.25rem' }}>
              {stats.por_disciplina?.Informática || 0}
            </div>
            <div style={{ color: '#718096', fontSize: '0.95rem' }}>Questões de Informática</div>
          </div>

          <div style={{
            background: 'white',
            padding: '1.5rem',
            borderRadius: '12px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>📖</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#4facfe', marginBottom: '0.25rem' }}>
              {Object.keys(stats.por_disciplina || {}).length}
            </div>
            <div style={{ color: '#718096', fontSize: '0.95rem' }}>Disciplinas</div>
          </div>

          <div style={{
            background: 'white',
            padding: '1.5rem',
            borderRadius: '12px',
            boxShadow: '0 4px 12px rgba(0,0,0,0.08)',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🎯</div>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#43e97b', marginBottom: '0.25rem' }}>
              54
            </div>
            <div style={{ color: '#718096', fontSize: '0.95rem' }}>Tópicos Disponíveis</div>
          </div>
        </div>
      )}

      {/* Cards de Acesso Rápido */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
        gap: '2rem',
        marginBottom: '3rem'
      }}>
        {cards.map((card, idx) => {
          const CardWrapper = card.action ? 'div' : Link
          const wrapperProps = card.action 
            ? { onClick: card.action, style: { cursor: 'pointer' } }
            : { to: card.link, style: { textDecoration: 'none' } }
          
          return (
            <CardWrapper
              key={idx}
              {...wrapperProps}
            >
              <div style={{
                background: card.gradient,
                padding: '2rem',
                borderRadius: '16px',
                color: 'white',
                height: '100%',
                boxShadow: card.highlight 
                  ? '0 20px 60px rgba(102, 126, 234, 0.4)' 
                  : '0 10px 30px rgba(0,0,0,0.2)',
                cursor: 'pointer',
                position: 'relative',
                overflow: 'hidden',
                transform: card.highlight ? 'scale(1.02)' : 'scale(1)',
                transition: 'all 0.3s ease',
                border: card.special ? '3px solid #FFD700' : 'none'
              }}
              onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
              onMouseLeave={(e) => e.currentTarget.style.transform = card.highlight ? 'scale(1.02)' : 'scale(1)'}
              >
                {card.highlight && (
                  <div style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    background: 'rgba(255,255,255,0.3)',
                    padding: '0.5rem 1rem',
                    borderRadius: '20px',
                    fontSize: '0.85rem',
                    fontWeight: 'bold'
                  }}>
                    {card.special ? '🔥 ESPECIAL' : '⭐ RECOMENDADO'}
                  </div>
                )}
              
              <h3 style={{
                margin: '0 0 1rem 0',
                fontSize: '1.8rem',
                fontWeight: 'bold'
              }}>
                {card.title}
              </h3>
              
              <p style={{
                margin: 0,
                fontSize: '1.1rem',
                opacity: 0.95,
                lineHeight: '1.6'
              }}>
                {card.description}
              </p>
              
              <div style={{
                marginTop: '1.5rem',
                display: 'inline-block',
                padding: '0.75rem 1.5rem',
                background: 'rgba(255,255,255,0.2)',
                borderRadius: '8px',
                fontWeight: 'bold',
                fontSize: '1rem'
              }}>
                Acessar →
              </div>
            </div>
          </CardWrapper>
        )})}
      </div>

      {/* Guia Rápido */}
      <div style={{
        background: 'white',
        padding: '2rem',
        borderRadius: '16px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.08)'
      }}>
        <h2 style={{ margin: '0 0 1.5rem 0', fontSize: '1.8rem', color: '#2d3748' }}>
          📋 Como Usar o Sistema
        </h2>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1.5rem'
        }}>
          <div>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              marginBottom: '1rem'
            }}>
              1
            </div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>Faça Provas Completas</h3>
            <p style={{ margin: 0, color: '#718096', lineHeight: '1.6' }}>
              Simule o concurso real com provas de 40-60 questões
            </p>
          </div>

          <div>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              marginBottom: '1rem'
            }}>
              2
            </div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>Gere Questões com IA</h3>
            <p style={{ margin: 0, color: '#718096', lineHeight: '1.6' }}>
              Crie questões personalizadas sobre qualquer tópico
            </p>
          </div>

          <div>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              marginBottom: '1rem'
            }}>
              3
            </div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>Pratique por Tópico</h3>
            <p style={{ margin: 0, color: '#718096', lineHeight: '1.6' }}>
              Foque nos seus pontos fracos estudando por disciplina
            </p>
          </div>

          <div>
            <div style={{
              width: '48px',
              height: '48px',
              borderRadius: '12px',
              background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
              color: 'white',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '1.5rem',
              marginBottom: '1rem'
            }}>
              4
            </div>
            <h3 style={{ margin: '0 0 0.5rem 0', fontSize: '1.1rem' }}>Acompanhe seu Progresso</h3>
            <p style={{ margin: 0, color: '#718096', lineHeight: '1.6' }}>
              Veja estatísticas e identifique áreas para melhorar
            </p>
          </div>
        </div>
      </div>

      {/* Dicas Finais */}
      <div style={{
        marginTop: '3rem',
        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        padding: '2rem',
        borderRadius: '16px',
        color: 'white'
      }}>
        <h2 style={{ margin: '0 0 1rem 0', fontSize: '1.5rem' }}>💡 Dicas de Ouro</h2>
        <ul style={{ margin: 0, paddingLeft: '1.5rem', lineHeight: '2' }}>
          <li><strong>Consistência é chave:</strong> Estude um pouco todos os dias</li>
          <li><strong>Foque em Informática:</strong> É 50% da prova!</li>
          <li><strong>Não negligencie Português:</strong> Interpretação de texto é fundamental</li>
          <li><strong>Pratique com tempo:</strong> Simule as condições reais da prova</li>
          <li><strong>Revise seus erros:</strong> Aprenda com cada questão</li>
        </ul>
      </div>
    </div>
  )
}

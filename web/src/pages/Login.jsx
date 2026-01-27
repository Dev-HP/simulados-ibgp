import { useState } from 'react'
import axios from 'axios'
import { API_URL } from '../config'

export default function Login({ onLogin }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)

      const response = await axios.post(`${API_URL}/api/token`, formData)
      
      // Salvar token
      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('username', username)
      
      // Configurar axios para usar o token
      axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access_token}`
      
      onLogin()
    } catch (err) {
      setError('Usuário ou senha inválidos')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '80vh' 
    }}>
      <div className="card" style={{ maxWidth: '400px', width: '100%' }}>
        <h1>Login</h1>
        <p style={{ marginBottom: '2rem', color: '#666' }}>
          Sistema de Simulados IBGP
        </p>

        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Usuário
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              style={{ width: '100%', padding: '0.5rem' }}
            />
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>
              Senha
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              style={{ width: '100%', padding: '0.5rem' }}
            />
          </div>

          {error && (
            <div style={{ 
              padding: '0.75rem', 
              background: '#f8d7da', 
              color: '#721c24',
              borderRadius: '4px',
              marginBottom: '1rem'
            }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ width: '100%' }}
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        <div style={{ 
          marginTop: '1.5rem', 
          padding: '1rem', 
          background: '#d1ecf1',
          borderRadius: '4px',
          fontSize: '0.9rem'
        }}>
          <strong>Credenciais de teste:</strong><br />
          Usuário: teste<br />
          Senha: teste123
        </div>
      </div>
    </div>
  )
}

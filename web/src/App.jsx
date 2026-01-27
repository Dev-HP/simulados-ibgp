import { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Home from './pages/Home'
import Simulados from './pages/Simulados'
import SimuladoExec from './pages/SimuladoExec'
import Results from './pages/Results'
import Analytics from './pages/Analytics'
import Upload from './pages/Upload'
import Login from './pages/Login'

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [username, setUsername] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    // Verificar se há token salvo
    const token = localStorage.getItem('token')
    const savedUsername = localStorage.getItem('username')
    
    if (token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
      setIsAuthenticated(true)
      setUsername(savedUsername || '')
    }
  }, [])

  const handleLogin = () => {
    setIsAuthenticated(true)
    setUsername(localStorage.getItem('username') || '')
    navigate('/')
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('username')
    delete axios.defaults.headers.common['Authorization']
    setIsAuthenticated(false)
    setUsername('')
    navigate('/')
  }

  if (!isAuthenticated) {
    return <Login onLogin={handleLogin} />
  }

  return (
    <div className="app">
      <nav className="navbar">
        <h1>Simulados IBGP</h1>
        <div className="nav-links">
          <Link to="/">Home</Link>
          <Link to="/upload">Upload Edital</Link>
          <Link to="/simulados">Simulados</Link>
          <Link to="/analytics">Analytics</Link>
          <button 
            onClick={handleLogout}
            style={{ 
              marginLeft: '1rem',
              padding: '0.5rem 1rem',
              background: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Sair ({username})
          </button>
        </div>
      </nav>
      
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/simulados" element={<Simulados />} />
          <Route path="/simulados/:id" element={<SimuladoExec />} />
          <Route path="/results" element={<Results />} />
          <Route path="/analytics" element={<Analytics />} />
        </Routes>
      </main>
    </div>
  )
}

export default App

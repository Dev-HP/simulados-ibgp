import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Simulados from './pages/Simulados'
import SimuladoExec from './pages/SimuladoExec'
import Results from './pages/Results'
import Analytics from './pages/Analytics'
import Upload from './pages/Upload'

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <h1>Simulados IBGP</h1>
        <div className="nav-links">
          <a href="/">Home</a>
          <a href="/upload">Upload Edital</a>
          <a href="/simulados">Simulados</a>
          <a href="/analytics">Analytics</a>
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

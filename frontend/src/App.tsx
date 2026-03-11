import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Segnalazioni from './pages/Segnalazioni'
import Asset from './pages/Asset'
import Interventi from './pages/Interventi'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const token = localStorage.getItem('access_token')
  return token ? <>{children}</> : <Navigate to="/login" replace />
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        <Route path="/segnalazioni" element={
          <PrivateRoute>
            <Segnalazioni />
          </PrivateRoute>
        } />
        <Route path="/asset" element={
          <PrivateRoute>
            <Asset />
          </PrivateRoute>
        } />
        <Route path="/interventi" element={
          <PrivateRoute>
            <Interventi />
          </PrivateRoute>
        } />
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
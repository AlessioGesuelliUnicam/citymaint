import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../lib/api'
import type { Intervento } from '../../lib/types'

export default function Interventi() {
  const navigate = useNavigate()
  const [interventi, setInterventi] = useState<Intervento[]>([])

  useEffect(() => {
    api.get('/api/v1/interventi/').then(r => setInterventi(r.data))
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-700">CityMaint — Tolentino</h1>
        <div className="flex gap-4 text-sm">
          <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-blue-600">Dashboard</button>
          <button onClick={() => navigate('/segnalazioni')} className="text-gray-600 hover:text-blue-600">Segnalazioni</button>
          <button onClick={() => navigate('/asset')} className="text-gray-600 hover:text-blue-600">Asset</button>
          <button onClick={() => navigate('/interventi')} className="text-blue-600 font-medium">Interventi</button>
          <button onClick={() => { localStorage.removeItem('access_token'); navigate('/login') }} className="text-gray-500 hover:text-red-500">Esci</button>
        </div>
      </nav>

      <main className="p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Interventi</h2>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr className="text-left text-gray-500">
                <th className="px-4 py-3">Titolo</th>
                <th className="px-4 py-3">Tipo</th>
                <th className="px-4 py-3">Stato</th>
                <th className="px-4 py-3">Data pianificata</th>
                <th className="px-4 py-3">Costo stimato</th>
              </tr>
            </thead>
            <tbody>
              {interventi.map(i => (
                <tr key={i.id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{i.title}</td>
                  <td className="px-4 py-3 capitalize">{i.type}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      i.status === 'pianificato' ? 'bg-blue-100 text-blue-700' :
                      i.status === 'in_corso' ? 'bg-yellow-100 text-yellow-700' :
                      i.status === 'completato' ? 'bg-green-100 text-green-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {i.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="px-4 py-3">{i.planned_date ?? '—'}</td>
                  <td className="px-4 py-3">{i.estimated_cost ? `€ ${i.estimated_cost}` : '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}
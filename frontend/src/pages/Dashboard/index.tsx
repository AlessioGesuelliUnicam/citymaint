import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../lib/api'
import type { Segnalazione, Intervento, AssetUrbano } from '../../lib/types'

export default function Dashboard() {
  const navigate = useNavigate()
  const [segnalazioni, setSegnalazioni] = useState<Segnalazione[]>([])
  const [interventi, setInterventi] = useState<Intervento[]>([])
  const [asset, setAsset] = useState<AssetUrbano[]>([])

  useEffect(() => {
    api.get('/api/v1/segnalazioni/').then(r => setSegnalazioni(r.data))
    api.get('/api/v1/interventi/').then(r => setInterventi(r.data))
    api.get('/api/v1/asset/').then(r => setAsset(r.data))
  }, [])

  const segnalazioniAperte = segnalazioni.filter(s => s.status === 'aperta').length
  const interventiInCorso = interventi.filter(i => i.status === 'in_corso').length

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-700">CityMaint — Tolentino</h1>
        <button
          onClick={() => { localStorage.removeItem('access_token'); navigate('/login') }}
          className="text-sm text-gray-500 hover:text-red-500"
        >
          Esci
        </button>
      </nav>

      <main className="p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-500">Segnalazioni aperte</p>
            <p className="text-4xl font-bold text-red-500 mt-1">{segnalazioniAperte}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-500">Interventi in corso</p>
            <p className="text-4xl font-bold text-yellow-500 mt-1">{interventiInCorso}</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <p className="text-sm text-gray-500">Asset monitorati</p>
            <p className="text-4xl font-bold text-blue-500 mt-1">{asset.length}</p>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-700 mb-4">Ultime segnalazioni</h3>
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b">
                <th className="pb-2">Codice</th>
                <th className="pb-2">Categoria</th>
                <th className="pb-2">Descrizione</th>
                <th className="pb-2">Stato</th>
              </tr>
            </thead>
            <tbody>
              {segnalazioni.slice(0, 5).map(s => (
                <tr key={s.id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="py-2 font-mono text-blue-600">{s.unique_code}</td>
                  <td className="py-2 capitalize">{s.category}</td>
                  <td className="py-2 text-gray-600 truncate max-w-xs">{s.description}</td>
                  <td className="py-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      s.status === 'aperta' ? 'bg-red-100 text-red-700' :
                      s.status === 'in_lavorazione' ? 'bg-yellow-100 text-yellow-700' :
                      s.status === 'completata' ? 'bg-green-100 text-green-700' :
                      'bg-gray-100 text-gray-700'
                    }`}>
                      {s.status.replace('_', ' ')}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}
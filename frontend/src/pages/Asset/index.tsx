import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../../lib/api'
import type { AssetUrbano } from '../../lib/types'

export default function Asset() {
  const navigate = useNavigate()
  const [asset, setAsset] = useState<AssetUrbano[]>([])

  useEffect(() => {
    api.get('/api/v1/asset/').then(r => setAsset(r.data))
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-700">CityMaint — Tolentino</h1>
        <div className="flex gap-4 text-sm">
          <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-blue-600">Dashboard</button>
          <button onClick={() => navigate('/segnalazioni')} className="text-gray-600 hover:text-blue-600">Segnalazioni</button>
          <button onClick={() => navigate('/asset')} className="text-blue-600 font-medium">Asset</button>
          <button onClick={() => navigate('/interventi')} className="text-gray-600 hover:text-blue-600">Interventi</button>
          <button onClick={() => { localStorage.removeItem('access_token'); navigate('/login') }} className="text-gray-500 hover:text-red-500">Esci</button>
        </div>
      </nav>

      <main className="p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Asset Urbani</h2>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 border-b">
              <tr className="text-left text-gray-500">
                <th className="px-4 py-3">Nome</th>
                <th className="px-4 py-3">Tipo</th>
                <th className="px-4 py-3">Health Score</th>
                <th className="px-4 py-3">Vita utile (anni)</th>
                <th className="px-4 py-3">Installazione</th>
              </tr>
            </thead>
            <tbody>
              {asset.map(a => (
                <tr key={a.id} className="border-b last:border-0 hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{a.name}</td>
                  <td className="px-4 py-3 capitalize">{a.type}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            Number(a.health_score) > 70 ? 'bg-green-500' :
                            Number(a.health_score) > 40 ? 'bg-yellow-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${a.health_score}%` }}
                        />
                      </div>
                      <span>{a.health_score}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3">{a.useful_life_years ?? '—'}</td>
                  <td className="px-4 py-3">{a.installation_date ?? '—'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </main>
    </div>
  )
}
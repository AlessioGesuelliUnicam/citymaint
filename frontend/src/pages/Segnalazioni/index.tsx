import { useEffect, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { useNavigate } from 'react-router-dom'
import api from '../../lib/api'
import type { Segnalazione } from '../../lib/types'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

// Fix icone Leaflet con Vite
import iconUrl from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'
L.Marker.prototype.options.icon = L.icon({ iconUrl, shadowUrl: iconShadow, iconAnchor: [12, 41] })

export default function Segnalazioni() {
  const navigate = useNavigate()
  const [segnalazioni, setSegnalazioni] = useState<Segnalazione[]>([])

  useEffect(() => {
    api.get('/api/v1/segnalazioni/').then(r => setSegnalazioni(r.data))
  }, [])

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-blue-700">CityMaint — Tolentino</h1>
        <div className="flex gap-4 text-sm">
          <button onClick={() => navigate('/dashboard')} className="text-gray-600 hover:text-blue-600">Dashboard</button>
          <button onClick={() => navigate('/segnalazioni')} className="text-blue-600 font-medium">Segnalazioni</button>
          <button onClick={() => navigate('/asset')} className="text-gray-600 hover:text-blue-600">Asset</button>
          <button onClick={() => navigate('/interventi')} className="text-gray-600 hover:text-blue-600">Interventi</button>
          <button onClick={() => { localStorage.removeItem('access_token'); navigate('/login') }} className="text-gray-500 hover:text-red-500">Esci</button>
        </div>
      </nav>

      <main className="p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">Segnalazioni</h2>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-lg shadow overflow-hidden" style={{ height: '500px' }}>
            <MapContainer
              center={[43.2097, 13.2833]}
              zoom={14}
              style={{ height: '100%', width: '100%' }}
            >
              <TileLayer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution='© OpenStreetMap'
              />
              {segnalazioni.map(s => (
                <Marker key={s.id} position={[s.latitude, s.longitude]}>
                  <Popup>
                    <strong>{s.unique_code}</strong><br />
                    {s.description}<br />
                    <span className="capitalize">{s.status}</span>
                  </Popup>
                </Marker>
              ))}
            </MapContainer>
          </div>

          <div className="bg-white rounded-lg shadow overflow-auto" style={{ height: '500px' }}>
            <table className="w-full text-sm">
              <thead className="sticky top-0 bg-white border-b">
                <tr className="text-left text-gray-500">
                  <th className="px-4 py-3">Codice</th>
                  <th className="px-4 py-3">Categoria</th>
                  <th className="px-4 py-3">Stato</th>
                </tr>
              </thead>
              <tbody>
                {segnalazioni.map(s => (
                  <tr key={s.id} className="border-b last:border-0 hover:bg-gray-50">
                    <td className="px-4 py-3 font-mono text-blue-600">{s.unique_code}</td>
                    <td className="px-4 py-3 capitalize">{s.category}</td>
                    <td className="px-4 py-3">
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
        </div>
      </main>
    </div>
  )
}
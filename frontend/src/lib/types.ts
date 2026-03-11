export interface Operatore {
  id: string
  name: string
  surname: string
  email: string
  role: 'operatore' | 'tecnico' | 'responsabile' | 'admin'
  is_active: boolean
  created_at: string
}

export interface Segnalazione {
  id: string
  unique_code: string
  category: string
  description: string
  latitude: number
  longitude: number
  status: 'aperta' | 'in_lavorazione' | 'completata' | 'rifiutata'
  ai_suggested_category: string | null
  ai_priority_score: number | null
  citizen_email: string | null
  created_at: string
}

export interface AssetUrbano {
  id: string
  type: string
  name: string
  latitude: number
  longitude: number
  installation_date: string | null
  useful_life_years: number | null
  health_score: number | null
  notes: string | null
  created_at: string
}

export interface Intervento {
  id: string
  title: string
  type: 'ordinario' | 'straordinario' | 'emergenza'
  status: 'pianificato' | 'in_corso' | 'completato' | 'annullato'
  asset_id: string
  squadra_id: string | null
  planned_date: string | null
  estimated_cost: number | null
  actual_cost: number | null
  notes: string | null
  created_at: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
}
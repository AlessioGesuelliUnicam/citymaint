import logging
from datetime import datetime
from typing import TypeVar, Type

import anthropic
from ollama import AsyncClient as OllamaAsyncClient
from pydantic import BaseModel

from app.core.config import settings
from app.models.enums import CategoriaSegnalazione
from app.schemas.ai import RispostaCategorizzazione, RispostaPrioritizzazione

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

_SYSTEM_CATEGORIZZAZIONE = """\
Sei un sistema di classificazione per segnalazioni di manutenzione urbana del Comune di Tolentino.
Classifica la segnalazione nella categoria più appropriata tra le seguenti:

- stradale: buche, dissesti del manto stradale, marciapiedi danneggiati, segnaletica orizzontale usurata
- illuminazione: lampioni spenti o danneggiati, cavi scoperti, problemi all'illuminazione pubblica
- verde_pubblico: alberi pericolanti, erba alta, danni a parchi o giardini pubblici, potatura necessaria
- rifiuti: abbandono di rifiuti, bidoni pieni o danneggiati, pulizia strade e aree pubbliche
- segnaletica: segnali stradali mancanti, danneggiati o illeggibili, semafori guasti, cartellonistica
- fognatura: tombini ostruiti o danneggiati, allagamenti, problemi fognari, odori da rete fognaria
- altro: segnalazioni che non rientrano nelle categorie precedenti (panchine, recinzioni, strutture varie)

Esempi:
- "Buca profonda in Via Roma" → stradale, confidence 0.95
- "Lampione spento da 3 giorni in Piazza Libertà" → illuminazione, confidence 0.98
- "Albero pericolante vicino alla scuola elementare" → verde_pubblico, confidence 0.92
- "Rifiuti abbandonati nel parcheggio di Via Milano" → rifiuti, confidence 0.97
- "Segnale di stop mancante all'incrocio con Via Verdi" → segnaletica, confidence 0.90
- "Tombino ostruito, rischio allagamento" → fognatura, confidence 0.94
- "Panchina rotta nel parco centrale" → altro, confidence 0.85

Rispondi ESCLUSIVAMENTE con un oggetto JSON valido, senza preambolo né markdown:
{"categoria": "<categoria>", "confidence": <float 0.0-1.0>, "motivazione": "<breve spiegazione>"}\
"""

_SYSTEM_PRIORITIZZAZIONE = """\
Sei un sistema di prioritizzazione per segnalazioni di manutenzione urbana del Comune di Tolentino.
Calcola uno score di priorità da 0.0 a 10.0 basandoti sui seguenti fattori e pesi:

1. Sicurezza pubblica (30%): parole chiave di rischio nel testo (buca profonda, lampione rotto, cavi scoperti,
   pericoloso, caduto, incidente, rischio) → contributo massimo 3.0
2. Segnalazioni vicine recenti (25%): più segnalazioni nelle vicinanze (50m, ultimi 30gg):
   0=+0.0, 1-2=+1.0, 3-5=+1.5, >5=+2.5
3. Anzianità (20%): più giorni è aperta → urgenza crescente:
   0gg=+0.0, 1-7gg=+0.5, 8-30gg=+1.0, >30gg=+2.0
4. Vicinanza zone sensibili (15%): scuole, ospedali, asili → se True aggiunge +1.5
5. Stagionalità (10%): boost +1.0 per categorie stradale/illuminazione nei mesi ottobre-marzo

Rispondi ESCLUSIVAMENTE con un oggetto JSON valido, senza preambolo né markdown:
{"score": <float 0.0-10.0>, "motivazione": "<spiegazione dettagliata dei fattori considerati>"}\
"""


class AIService:

    def __init__(self) -> None:
        self.provider = settings.AI_PROVIDER
        if self.provider == "ollama":
            self._ollama = OllamaAsyncClient(host=settings.OLLAMA_BASE_URL)
            self._anthropic = None
        else:
            self._anthropic = anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            self._ollama = None

    async def _chiama_anthropic(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[T],
    ) -> str:
        response = await self._anthropic.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text.strip()

    async def _chiama_ollama(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[T],
    ) -> str:
        response = await self._ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            format=schema.model_json_schema(),
            options={"temperature": 0},
        )
        return response.message.content

    async def categorizza(
        self,
        descrizione: str,
        indirizzo: str | None = None,
    ) -> RispostaCategorizzazione:
        fallback = RispostaCategorizzazione(
            categoria=CategoriaSegnalazione.DA_VERIFICARE,
            confidence=0.0,
            motivazione="Classificazione automatica non disponibile",
        )

        if self.provider == "anthropic" and not settings.ANTHROPIC_API_KEY:
            logger.warning("[AI] ANTHROPIC_API_KEY non configurata — skip categorizzazione")
            return fallback

        user_prompt = f"Descrizione: {descrizione}"
        if indirizzo:
            user_prompt += f"\nIndirizzo: {indirizzo}"

        try:
            logger.info("[AI:%s] Categorizzazione avviata | input: %.200s", self.provider, user_prompt)

            if self.provider == "ollama":
                raw = await self._chiama_ollama(_SYSTEM_CATEGORIZZAZIONE, user_prompt, RispostaCategorizzazione)
            else:
                raw = await self._chiama_anthropic(_SYSTEM_CATEGORIZZAZIONE, user_prompt, RispostaCategorizzazione)

            logger.info("[AI:%s] Categorizzazione completata | output: %.500s", self.provider, raw)

            result = RispostaCategorizzazione.model_validate_json(raw)

            if result.confidence < 0.6:
                logger.info(
                    "[AI:%s] Confidence bassa (%.2f) → categoria forzata a da_verificare",
                    self.provider,
                    result.confidence,
                )
                result.categoria = CategoriaSegnalazione.DA_VERIFICARE

            return result

        except Exception as e:
            logger.error("[AI:%s] Errore categorizzazione: %s", self.provider, e)
            fallback.motivazione = f"Errore AI ({self.provider}): {e}"
            return fallback

    async def calcola_priorita(
        self,
        descrizione: str,
        categoria: str,
        numero_segnalazioni_vicine: int = 0,
        giorni_apertura: int = 0,
        vicino_zona_sensibile: bool = False,
    ) -> RispostaPrioritizzazione:
        fallback = RispostaPrioritizzazione(
            score=5.0,
            motivazione="Calcolo priorità automatico non disponibile",
        )

        if self.provider == "anthropic" and not settings.ANTHROPIC_API_KEY:
            logger.warning("[AI] ANTHROPIC_API_KEY non configurata — skip prioritizzazione")
            return fallback

        mese = datetime.now().month
        stagione = "invernale (ottobre-marzo)" if mese in (10, 11, 12, 1, 2, 3) else "non invernale"

        user_prompt = (
            f"Descrizione: {descrizione}\n"
            f"Categoria: {categoria}\n"
            f"Segnalazioni vicine (50m, ultimi 30gg): {numero_segnalazioni_vicine}\n"
            f"Giorni di apertura: {giorni_apertura}\n"
            f"Vicino a zona sensibile (scuola/ospedale): {'sì' if vicino_zona_sensibile else 'no'}\n"
            f"Stagione corrente: {stagione}"
        )

        try:
            logger.info("[AI:%s] Prioritizzazione avviata | input: %.200s", self.provider, user_prompt)

            if self.provider == "ollama":
                raw = await self._chiama_ollama(_SYSTEM_PRIORITIZZAZIONE, user_prompt, RispostaPrioritizzazione)
            else:
                raw = await self._chiama_anthropic(_SYSTEM_PRIORITIZZAZIONE, user_prompt, RispostaPrioritizzazione)

            logger.info("[AI:%s] Prioritizzazione completata | output: %.500s", self.provider, raw)

            return RispostaPrioritizzazione.model_validate_json(raw)

        except Exception as e:
            logger.error("[AI:%s] Errore prioritizzazione: %s", self.provider, e)
            fallback.motivazione = f"Errore AI ({self.provider}): {e}"
            return fallback

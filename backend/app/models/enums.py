import enum


class RuoloOperatore(str, enum.Enum):
    OPERATORE = "operatore"
    TECNICO = "tecnico"
    RESPONSABILE = "responsabile"
    ADMIN = "admin"

class CategoriaSegnalazione(str, enum.Enum):
    STRADALE = "stradale"
    ILLUMINAZIONE = "illuminazione"
    VERDE_PUBBLICO = "verde_pubblico"
    RIFIUTI = "rifiuti"
    SEGNALETICA = "segnaletica"
    FOGNATURA = "fognatura"
    ALTRO = "altro"
    DA_VERIFICARE = "da_verificare"


class StatoSegnalazione(str, enum.Enum):
    APERTA = "aperta"
    IN_LAVORAZIONE = "in_lavorazione"
    COMPLETATA = "completata"
    RIFIUTATA = "rifiutata"


class TipoAsset(str, enum.Enum):
    STRADA = "strada"
    LAMPIONE = "lampione"
    PARCO = "parco"
    SEMAFORO = "semaforo"
    TOMBINO = "tombino"
    ALTRO = "altro"


class TipoIntervento(str, enum.Enum):
    ORDINARIO = "ordinario"
    STRAORDINARIO = "straordinario"
    EMERGENZA = "emergenza"


class StatoIntervento(str, enum.Enum):
    PIANIFICATO = "pianificato"
    IN_CORSO = "in_corso"
    COMPLETATO = "completato"
    ANNULLATO = "annullato"
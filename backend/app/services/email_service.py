import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.core.config import settings


class EmailService:

    @staticmethod
    async def send(
        to: str,
        subject: str,
        html: str,
    ) -> bool:
        if not settings.EMAIL_ENABLED:
            print(f"[EMAIL DISABLED] To: {to} | Subject: {subject}")
            return True

        if settings.EMAIL_PROVIDER == "smtp":
            return await EmailService._send_smtp(to, subject, html)

        print(f"[EMAIL] Provider '{settings.EMAIL_PROVIDER}' non supportato")
        return False

    @staticmethod
    async def _send_smtp(to: str, subject: str, html: str) -> bool:
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
            msg["To"] = to
            msg.attach(MIMEText(html, "html"))

            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.sendmail(settings.EMAIL_FROM, to, msg.as_string())

            return True
        except Exception as e:
            print(f"[EMAIL ERROR] {e}")
            return False

    @staticmethod
    async def send_conferma_segnalazione(
        to: str,
        unique_code: str,
        description: str,
    ) -> bool:
        subject = f"Segnalazione {unique_code} ricevuta — Comune di Tolentino"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #1d4ed8;">Comune di Tolentino</h2>
            <p>La sua segnalazione è stata ricevuta correttamente.</p>
            <div style="background: #f3f4f6; padding: 16px; border-radius: 8px; margin: 16px 0;">
                <p><strong>Codice segnalazione:</strong> {unique_code}</p>
                <p><strong>Descrizione:</strong> {description}</p>
            </div>
            <p>Può verificare lo stato della sua segnalazione in qualsiasi momento 
            usando il codice <strong>{unique_code}</strong>.</p>
            <p style="color: #6b7280; font-size: 12px;">
                Comune di Tolentino — Ufficio Manutenzione Urbana
            </p>
        </div>
        """
        return await EmailService.send(to, subject, html)

    @staticmethod
    async def send_aggiornamento_stato(
        to: str,
        unique_code: str,
        nuovo_stato: str,
    ) -> bool:
        stati = {
            "in_lavorazione": "presa in carico",
            "completata": "risolta",
            "rifiutata": "non accettata",
        }
        stato_leggibile = stati.get(nuovo_stato, nuovo_stato)
        subject = f"Aggiornamento segnalazione {unique_code} — Comune di Tolentino"
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #1d4ed8;">Comune di Tolentino</h2>
            <p>La sua segnalazione <strong>{unique_code}</strong> è stata 
            <strong>{stato_leggibile}</strong>.</p>
            <p style="color: #6b7280; font-size: 12px;">
                Comune di Tolentino — Ufficio Manutenzione Urbana
            </p>
        </div>
        """
        return await EmailService.send(to, subject, html)
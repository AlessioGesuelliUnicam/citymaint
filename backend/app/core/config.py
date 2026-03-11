from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "CityMaint"
    PROJECT_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5433
    POSTGRES_USER: str = "citymaint"
    POSTGRES_PASSWORD: str = "citymaint_dev"
    POSTGRES_DB: str = "citymaint_db"

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # Sicurezza
    SECRET_KEY: str = "cambia_questa_chiave_in_produzione"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 ore

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # AI
    ANTHROPIC_API_KEY: str = ""

    # Email
    EMAIL_ENABLED: bool = False
    EMAIL_PROVIDER: str = "smtp"  # smtp | sendgrid | resend
    EMAIL_FROM: str = "noreply@comune.tolentino.mc.it"
    EMAIL_FROM_NAME: str = "Comune di Tolentino — CityMaint"
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
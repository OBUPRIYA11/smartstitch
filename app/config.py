from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SmartStitch"
    postgres_url: str = "postgresql+psycopg2://smartstitch:smartstitch@localhost:5432/smartstitch"
    mongo_url: str = "mongodb://localhost:27017"
    mongo_db: str = "smartstitch"

    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_from_number: str = ""
    sms_target_number: str = ""

    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    notification_email_to: str = ""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

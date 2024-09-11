from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    environment: str = "DEV"
    twilio_account_sid: str = ""
    twilio_auth_token: str = ""
    twilio_phone_number: str = ""
    db_name: str = "snapshot"
    hash_secret: str = "test"
    admin_pass: str = "definitely_not_admin"
    beta_code: str = "test"
    beta_allowlist: str = ""


settings = Settings()

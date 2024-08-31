from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    environment: str
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str
    db_name: str
    hash_secret: str
    admin_pass: str
    dev_code: str
    dev_allowlist: str


settings = Settings()

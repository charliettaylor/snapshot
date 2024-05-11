from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str

    class Config:
        env_file = ".env"

settings = Settings()

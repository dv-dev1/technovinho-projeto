from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "postgresql+psycopg2://technovinho:technovinho@localhost:5432/technovinho"
    jwt_secret: str = "dev-secret-change-me"
    jwt_expire_hours: int = 24
    cors_origins: str = "http://localhost:8501,http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()

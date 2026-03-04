from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="allow"
    )

class DatabaseSettings(CommonSettings):
    database_url: str
    database_echo: bool

class TokenSettings(CommonSettings):
    private_key_path: str
    public_key_path: str
    token_algorithm: str
    token_type: str
    token_access_expires: int
    token_refresh_expires: int

class Settings:
    database_settings: DatabaseSettings = DatabaseSettings()
    token_settings: TokenSettings = TokenSettings()

settings = Settings()

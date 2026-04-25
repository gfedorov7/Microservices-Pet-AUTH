from typing import List

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
    token_algorithm: str
    token_type: str
    token_access_expires: int
    token_refresh_expires: int

class PasswordParamsSettings(BaseSettings):
    len_password: int = 8
    available_spec_symbols: List[str] = ["/", "$", "@", ".", "_", "-"]

class KeysSettings(CommonSettings):
    private_key_path: str
    public_key_path: str

    @property
    def private_key(self) -> bytes:
        return self._read_file(self.private_key_path)

    @property
    def public_key(self) -> bytes:
        return self._read_file(self.public_key_path)

    @staticmethod
    def _read_file(path: str) -> bytes:
        with open(path, "rb") as f:
            return f.read()

class RedisSettings(CommonSettings):
    redis_host: str
    redis_port: int
    redis_decode_responses: bool

class KafkaSettings(CommonSettings):
    kafka_broker_id: int
    kafka_zookeeper_connect: str
    kafka_advertised_listeners: str
    kafka_offsets_topic_replication_factor: int

class Settings:
    database_settings: DatabaseSettings = DatabaseSettings()
    token_settings: TokenSettings = TokenSettings()
    password_params_settings: PasswordParamsSettings = PasswordParamsSettings()
    keys_settings: KeysSettings = KeysSettings()
    redis_settings: RedisSettings = RedisSettings()
    kafka_settings: KafkaSettings = KafkaSettings()

settings = Settings()

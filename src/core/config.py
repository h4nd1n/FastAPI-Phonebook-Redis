from dataclasses import dataclass

from environs import Env


@dataclass
class RedisConfig:
    host: str = "127.0.0.1"
    port: int = 6379
    db: int = 0
    password: str | None = None
    key_prefix: str = "phonebook:"

    @staticmethod
    def from_env(env: Env) -> "RedisConfig":
        return RedisConfig(
            host=env.str("REDIS_HOST", "127.0.0.1"),
            port=env.int("REDIS_PORT", 6379),
            db=env.int("REDIS_DB", 0),
            password=env.str("REDIS_PASSWORD", default=None),
            key_prefix=env.str("REDIS_KEY_PREFIX", "phonebook:"),
        )


@dataclass
class Config:
    redis: RedisConfig


def load_config(env: Env | None = None, path: str | None = None) -> Config:
    if env is None:
        env = Env()
        env.read_env(path)
    return Config(redis=RedisConfig.from_env(env))

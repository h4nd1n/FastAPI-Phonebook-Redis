from src.core.config import Config, RedisConfig, load_config


class DummyEnv:
    def __init__(self, values: dict[str, str]):
        self.values = values

    def str(self, key: str, default=None):
        return self.values.get(key, default)

    def int(self, key: str, default=None):
        value = self.values.get(key, default)
        return int(value) if value is not None else value


def test_load_config_from_custom_env():
    env = DummyEnv(
        {
            "REDIS_HOST": "redis-host",
            "REDIS_PORT": "1234",
            "REDIS_DB": "2",
            "REDIS_PASSWORD": "secret",
            "REDIS_KEY_PREFIX": "custom:",
        }
    )

    config = load_config(env=env)

    assert isinstance(config, Config)
    assert config.redis == RedisConfig(
        host="redis-host",
        port=1234,
        db=2,
        password="secret",
        key_prefix="custom:",
    )


def test_load_config_defaults_when_env_missing():
    env = DummyEnv({})

    config = load_config(env=env)

    assert config.redis == RedisConfig()

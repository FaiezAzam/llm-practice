import logging
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openrouter_api_key: str
    default_model: str = "openrouter/free"
    max_retries: int = 3
    retry_delay: float = 2.0
    request_timeout: int = 30
    fallback_models: str = "openrouter/free"
    model_config = {"env_file": ".env"}

settings = Settings()


def setup_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )


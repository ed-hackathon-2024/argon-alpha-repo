from loguru import logger
from openai import AsyncOpenAI


class Manager:
    @property
    def client(self) -> AsyncOpenAI:
        return self._client

    @property
    def model(self) -> str:
        return self._model

    def __init__(self, model, api_key: str):
        self._model = model
        self._client = AsyncOpenAI(api_key=api_key)
        logger.debug("Manager initialised.")
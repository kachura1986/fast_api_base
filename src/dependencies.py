import logging
from dataclasses import dataclass
from functools import lru_cache

from fastapi import Request

from core.logger import setup_logging
from core.config import settings


# Logger
@lru_cache()
def get_logger() -> logging.Logger:
    return setup_logging(settings.LOGS_DIR / 'app.log')


# DI container
@dataclass
class PipelineDependencies:
    """General dependencies."""

    @classmethod
    async def create(cls) -> "PipelineDependencies":
        return cls()

    async def close(self) -> None:
        """Close all resources."""
        pass

# Example
# @dataclass
# class PipelineDependencies:
#     openai_client: AsyncAzureOpenAI
#
#     @classmethod
#     async def create(cls) -> "PipelineDependencies":
#         logger = get_logger()
#         openai_client = None
#
#         try:
#             openai_client = AsyncAzureOpenAI(
#                 api_key=settings.AZURE_OPENAI_API_KEY,
#                 azure_endpoint=settings.AZURE_OPENAI_ENDPOINT.rstrip("/"),
#                 api_version=settings.OPENAI_API_VERSION,
#                 timeout=20.0,
#                 max_retries=0,
#             )
#
#             return cls(
#                 openai_client=openai_client,
#             )
#
#         except BaseException:
#             logger.exception("Failed to initialize pipeline dependencies")
#
#             if openai_client is not None:
#                 try:
#                     await openai_client.close()
#                 except Exception:
#                     logger.exception("Failed to close OpenAI client")
#
#             raise
#
#     async def close(self) -> None:
#         logger = get_logger()
#
#         for name, resource in (
#                 ("Azure OpenAI client", self.openai_client),
#         ):
#             try:
#                 await resource.close()
#             except Exception:
#                 logger.exception("Failed to close %s", name)


# Dependency providers
def get_pipeline_dependencies(request: Request) -> PipelineDependencies:
    return request.app.state.dependencies

# Other dependencies

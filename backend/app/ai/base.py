import abc
from app.ai.schemas import AIReviewResult

class AIProvider(abc.ABC):
    @abc.abstractmethod
    async def review(self, prompt: str) -> AIReviewResult:
        """
        Send a prompt to the AI provider and return a structured review result.
        """
        pass

    @abc.abstractmethod
    async def is_available(self) -> bool:
        """
        Check if the AI provider is reachable.
        """
        pass

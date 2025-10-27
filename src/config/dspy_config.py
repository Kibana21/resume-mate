"""DSPy configuration and initialization"""

import os
from typing import Literal, Optional
import dspy
from loguru import logger

from .settings import get_settings


class DSPyConfig:
    """DSPy configuration and initialization"""

    def __init__(
        self,
        model_provider: Optional[Literal["openai", "anthropic", "azure"]] = None,
        model_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize DSPy configuration

        Args:
            model_provider: LLM provider (defaults to settings)
            model_name: Model name (defaults to settings)
            temperature: Temperature (defaults to settings)
            max_tokens: Max tokens (defaults to settings)
        """
        settings = get_settings()

        self.model_provider = model_provider or settings.llm_provider
        self.model_name = model_name or settings.llm_model
        self.temperature = temperature if temperature is not None else settings.llm_temperature
        self.max_tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

        # API Keys
        self.openai_api_key = settings.openai_api_key
        self.anthropic_api_key = settings.anthropic_api_key
        self.azure_openai_api_key = settings.azure_openai_api_key

    def initialize_lm(self) -> dspy.LM:
        """
        Initialize DSPy language model

        Returns:
            Configured DSPy LM instance

        Raises:
            ValueError: If provider is unsupported or API key is missing
        """
        logger.info(
            f"Initializing DSPy with provider: {self.model_provider}, "
            f"model: {self.model_name}, temperature: {self.temperature}"
        )

        if self.model_provider == "openai":
            if not self.openai_api_key:
                raise ValueError("OPENAI_API_KEY not set")

            lm = dspy.OpenAI(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.openai_api_key,
            )

        elif self.model_provider == "anthropic":
            if not self.anthropic_api_key:
                raise ValueError("ANTHROPIC_API_KEY not set")

            lm = dspy.Claude(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.anthropic_api_key,
            )

        elif self.model_provider == "azure":
            if not self.azure_openai_api_key:
                raise ValueError("AZURE_OPENAI_API_KEY not set")

            lm = dspy.AzureOpenAI(
                model=self.model_name,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                api_key=self.azure_openai_api_key,
            )

        else:
            raise ValueError(f"Unsupported provider: {self.model_provider}")

        # Configure DSPy settings
        dspy.settings.configure(lm=lm)

        logger.success(f"✓ DSPy initialized with {self.model_provider}/{self.model_name}")

        return lm

    @classmethod
    def from_settings(cls) -> "DSPyConfig":
        """Create DSPy config from application settings"""
        return cls()


# Global DSPy initialization function
def init_dspy() -> dspy.LM:
    """Initialize DSPy with default settings"""
    config = DSPyConfig.from_settings()
    return config.initialize_lm()

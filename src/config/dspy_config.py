"""DSPy configuration and initialization for Azure OpenAI"""

import os
from typing import Optional
import dspy
from loguru import logger

from .settings import get_settings


class DSPyConfig:
    """DSPy configuration and initialization for Azure OpenAI"""

    def __init__(
        self,
        deployment_name: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ):
        """
        Initialize DSPy configuration for Azure OpenAI

        Args:
            deployment_name: Azure OpenAI deployment name (defaults to settings)
            temperature: Temperature (defaults to settings)
            max_tokens: Max tokens (defaults to settings)
        """
        settings = get_settings()

        # Azure OpenAI configuration
        self.api_key = settings.azure_openai_api_key
        self.endpoint = settings.azure_openai_endpoint
        self.deployment_name = deployment_name or settings.azure_openai_deployment_name
        self.api_version = settings.azure_openai_api_version

        # LLM parameters
        self.temperature = temperature if temperature is not None else settings.llm_temperature
        self.max_tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens

    def initialize_lm(self) -> dspy.LM:
        """
        Initialize DSPy language model with Azure OpenAI

        Returns:
            Configured DSPy LM instance

        Raises:
            ValueError: If Azure OpenAI configuration is missing
        """
        logger.info(
            f"Initializing DSPy with Azure OpenAI - "
            f"Deployment: {self.deployment_name}, "
            f"Temperature: {self.temperature}, "
            f"Max Tokens: {self.max_tokens}"
        )

        # Validate required configuration
        if not self.api_key:
            raise ValueError("AZURE_OPENAI_API_KEY not set in environment variables")

        if not self.endpoint:
            raise ValueError("AZURE_OPENAI_ENDPOINT not set in environment variables")

        if not self.deployment_name:
            raise ValueError("AZURE_OPENAI_DEPLOYMENT_NAME not set in environment variables")

        if not self.api_version:
            raise ValueError("AZURE_OPENAI_API_VERSION not set in environment variables")

        # Initialize Azure OpenAI LM using dspy.LM
        self.lm = dspy.LM(
            self.deployment_name,
            api_key=self.api_key,
            api_base=self.endpoint,
            api_version=self.api_version
        )

        # Configure DSPy settings
        dspy.settings.configure(lm=self.lm)

        logger.success(
            f"✓ DSPy initialized with Azure OpenAI - "
            f"Deployment: {self.deployment_name}, "
            f"Endpoint: {self.endpoint}"
        )

        return self.lm

    @classmethod
    def from_settings(cls) -> "DSPyConfig":
        """Create DSPy config from application settings"""
        return cls()


# Global DSPy initialization function
def init_dspy() -> dspy.LM:
    """
    Initialize DSPy with Azure OpenAI using default settings

    Returns:
        Configured DSPy LM instance

    Example:
        >>> from src.config import init_dspy
        >>> lm = init_dspy()
        >>> # DSPy is now ready to use
    """
    config = DSPyConfig.from_settings()
    return config.initialize_lm()

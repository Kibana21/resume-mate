"""Configuration management for Resume Mate platform"""

from .settings import Settings, get_settings
from .dspy_config import DSPyConfig
from .division_config import (
    DIVISION_CONTEXTS,
    DIVISION_EXTRACTION_CONFIG,
    DivisionContextProvider,
    get_extraction_config,
)

__all__ = [
    "Settings",
    "get_settings",
    "DSPyConfig",
    "DIVISION_CONTEXTS",
    "DIVISION_EXTRACTION_CONFIG",
    "DivisionContextProvider",
    "get_extraction_config",
]

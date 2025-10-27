"""Application settings using Pydantic BaseSettings"""

from functools import lru_cache
from typing import List, Literal
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration settings"""

    # Application
    app_name: str = "Resume Mate"
    app_version: str = "0.1.0"
    debug: bool = Field(default=False, env="DEBUG")

    # LLM Configuration
    llm_provider: Literal["openai", "anthropic", "azure"] = Field(
        default="openai", env="LLM_PROVIDER"
    )
    llm_model: str = Field(default="gpt-4-turbo-preview", env="LLM_MODEL")
    llm_temperature: float = Field(default=0.0, env="LLM_TEMPERATURE")
    llm_max_tokens: int = Field(default=4000, env="LLM_MAX_TOKENS")

    # API Keys
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    anthropic_api_key: str = Field(default="", env="ANTHROPIC_API_KEY")
    azure_openai_api_key: str = Field(default="", env="AZURE_OPENAI_API_KEY")

    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/resume_mate",
        env="DATABASE_URL",
    )
    database_pool_size: int = Field(default=10, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=20, env="DATABASE_MAX_OVERFLOW")

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    redis_max_connections: int = Field(default=50, env="REDIS_MAX_CONNECTIONS")

    # Celery
    celery_broker_url: str = Field(default="redis://localhost:6379/1", env="CELERY_BROKER_URL")
    celery_result_backend: str = Field(
        default="redis://localhost:6379/2", env="CELERY_RESULT_BACKEND"
    )

    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")
    api_workers: int = Field(default=4, env="API_WORKERS")
    api_reload: bool = Field(default=True, env="API_RELOAD")

    # Security
    secret_key: str = Field(default="change-me-in-production", env="SECRET_KEY")
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="ALLOWED_ORIGINS",
    )
    jwt_secret_key: str = Field(default="change-me", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="JWT_ALGORITHM")
    jwt_expiration_minutes: int = Field(default=60, env="JWT_EXPIRATION_MINUTES")

    # File Storage
    upload_dir: str = Field(default="./data/uploads", env="UPLOAD_DIR")
    max_upload_size_mb: int = Field(default=10, env="MAX_UPLOAD_SIZE_MB")
    allowed_extensions: List[str] = Field(
        default=[".pdf", ".docx", ".doc", ".txt"], env="ALLOWED_EXTENSIONS"
    )

    # Feature Flags
    enable_ocr: bool = Field(default=True, env="ENABLE_OCR")
    enable_division_classification: bool = Field(
        default=True, env="ENABLE_DIVISION_CLASSIFICATION"
    )
    enable_hr_insights: bool = Field(default=True, env="ENABLE_HR_INSIGHTS")
    enable_quality_scoring: bool = Field(default=True, env="ENABLE_QUALITY_SCORING")
    strict_extraction_mode: bool = Field(default=False, env="STRICT_EXTRACTION_MODE")

    # DSPy
    dspy_cache_dir: str = Field(default="./.dspy_cache", env="DSPY_CACHE_DIR")
    dspy_traces_dir: str = Field(default="./logs/dspy_traces", env="DSPY_TRACES_DIR")
    enable_dspy_optimization: bool = Field(default=False, env="ENABLE_DSPY_OPTIMIZATION")

    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_file: str = Field(default="./logs/app.log", env="LOG_FILE")
    log_max_size_mb: int = Field(default=100, env="LOG_MAX_SIZE_MB")
    log_backup_count: int = Field(default=5, env="LOG_BACKUP_COUNT")

    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")

    # Division Configuration
    default_division: str = Field(default="technology", env="DEFAULT_DIVISION")
    enable_multi_division_support: bool = Field(
        default=True, env="ENABLE_MULTI_DIVISION_SUPPORT"
    )

    # Extraction Timeouts
    cv_extraction_timeout: int = Field(default=120, env="CV_EXTRACTION_TIMEOUT")
    jd_extraction_timeout: int = Field(default=60, env="JD_EXTRACTION_TIMEOUT")
    matching_timeout: int = Field(default=30, env="MATCHING_TIMEOUT")

    # Performance
    batch_size: int = Field(default=10, env="BATCH_SIZE")
    max_concurrent_extractions: int = Field(default=5, env="MAX_CONCURRENT_EXTRACTIONS")
    enable_caching: bool = Field(default=True, env="ENABLE_CACHING")
    cache_ttl_seconds: int = Field(default=3600, env="CACHE_TTL_SECONDS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()

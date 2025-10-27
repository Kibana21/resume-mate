"""
Extraction and matching pipelines for Resume Mate.

This package contains end-to-end pipelines for:
- CV/resume extraction
- Job description extraction
- CV-JD matching and evaluation
"""

from .cv_extraction_pipeline import CVExtractionPipeline
from .jd_extraction_pipeline import JDExtractionPipeline

__all__ = [
    "CVExtractionPipeline",
    "JDExtractionPipeline",
]

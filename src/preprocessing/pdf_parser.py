"""
PDF and DOCX parsing utilities.

Extracts text from PDF and DOCX files for CV/JD processing.
"""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def parse_pdf(file_path: str) -> str:
    """
    Extract text from PDF file.

    Args:
        file_path: Path to PDF file

    Returns:
        Extracted text content

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If parsing fails
    """
    try:
        import pdfplumber
    except ImportError:
        logger.error("pdfplumber not installed. Run: pip install pdfplumber")
        raise ImportError("pdfplumber is required. Install with: pip install pdfplumber")

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Parsing PDF: {file_path}")

    try:
        text_content = []
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_content.append(text)
                    logger.debug(f"Extracted text from page {page_num}")

        full_text = "\n\n".join(text_content)
        logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
        return full_text

    except Exception as e:
        logger.error(f"Error parsing PDF {file_path}: {e}")
        raise


def parse_docx(file_path: str) -> str:
    """
    Extract text from DOCX file.

    Args:
        file_path: Path to DOCX file

    Returns:
        Extracted text content

    Raises:
        FileNotFoundError: If file doesn't exist
        Exception: If parsing fails
    """
    try:
        from docx import Document
    except ImportError:
        logger.error("python-docx not installed. Run: pip install python-docx")
        raise ImportError("python-docx is required. Install with: pip install python-docx")

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Parsing DOCX: {file_path}")

    try:
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        full_text = "\n\n".join(paragraphs)

        logger.info(f"Successfully extracted {len(full_text)} characters from DOCX")
        return full_text

    except Exception as e:
        logger.error(f"Error parsing DOCX {file_path}: {e}")
        raise


def parse_txt(file_path: str) -> str:
    """
    Read text from TXT file.

    Args:
        file_path: Path to TXT file

    Returns:
        File content

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Reading TXT: {file_path}")

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    logger.info(f"Successfully read {len(text)} characters from TXT")
    return text


def parse_file(file_path: str) -> str:
    """
    Parse file and extract text (auto-detects format).

    Supports: PDF, DOCX, DOC, TXT

    Args:
        file_path: Path to file

    Returns:
        Extracted text content

    Raises:
        ValueError: If file format is unsupported
        FileNotFoundError: If file doesn't exist
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    extension = file_path.suffix.lower()

    if extension == '.pdf':
        return parse_pdf(str(file_path))
    elif extension in ['.docx', '.doc']:
        return parse_docx(str(file_path))
    elif extension == '.txt':
        return parse_txt(str(file_path))
    else:
        raise ValueError(
            f"Unsupported file format: {extension}. "
            f"Supported formats: .pdf, .docx, .doc, .txt"
        )


def get_file_info(file_path: str) -> dict:
    """
    Get basic file information.

    Args:
        file_path: Path to file

    Returns:
        Dictionary with file info
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    return {
        "file_name": file_path.name,
        "file_size_mb": file_path.stat().st_size / (1024 * 1024),
        "file_extension": file_path.suffix.lower(),
        "absolute_path": str(file_path.absolute()),
    }

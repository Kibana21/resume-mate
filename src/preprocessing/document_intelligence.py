"""
Azure Document Intelligence integration for document parsing.

Provides advanced document parsing capabilities using Azure AI Document Intelligence,
which extracts text with better structure preservation than basic PDF parsing.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
import os
import tempfile

# Ensure .env is loaded for Azure Document Intelligence credentials
try:
    from dotenv import load_dotenv
    env_file = Path(__file__).parent.parent.parent / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)  # Don't override existing env vars
except ImportError:
    pass  # dotenv not installed

logger = logging.getLogger(__name__)


def parse_document_to_markdown(file_path: str, endpoint: Optional[str] = None, key: Optional[str] = None) -> str:
    """
    Parse document using Azure Document Intelligence and convert to markdown.

    This provides much better structure preservation than basic PDF parsing,
    including proper heading detection, table extraction, and layout analysis.

    Args:
        file_path: Path to document file (PDF, DOCX, JPG, PNG, etc.)
        endpoint: Azure Document Intelligence endpoint (or use env var)
        key: Azure Document Intelligence key (or use env var)

    Returns:
        Document content in markdown format

    Raises:
        ImportError: If azure-ai-documentintelligence is not installed
        ValueError: If credentials are not provided
        FileNotFoundError: If file doesn't exist
    """
    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential
    except ImportError:
        logger.error("azure-ai-documentintelligence not installed")
        raise ImportError(
            "azure-ai-documentintelligence is required. "
            "Install with: pip install azure-ai-documentintelligence"
        )

    # Get credentials from parameters or environment
    endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence credentials not provided. "
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY "
            "in environment variables or pass as parameters."
        )

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Parsing document with Azure Document Intelligence: {file_path}")

    # Initialize Document Intelligence client
    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Analyze document with layout model (converts to markdown)
    logger.info("Analyzing document layout...")

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=f,
            content_type="application/octet-stream",
            output_content_format="markdown",  # Get markdown output
            pages="1-",  # Extract ALL pages (1 to end)
        )

    result = poller.result()

    # Extract markdown content
    markdown_content = result.content

    logger.info(f"Successfully extracted {len(markdown_content)} characters as markdown")
    logger.info(f"Detected {len(result.pages)} pages")

    return markdown_content


def parse_document_to_structured_data(
    file_path: str,
    endpoint: Optional[str] = None,
    key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Parse document using Azure Document Intelligence and return structured data.

    Returns both markdown content and additional metadata like tables, key-value pairs, etc.

    Args:
        file_path: Path to document file
        endpoint: Azure Document Intelligence endpoint
        key: Azure Document Intelligence key

    Returns:
        Dictionary with:
            - markdown: Markdown content
            - pages: Number of pages
            - tables: Extracted tables (if any)
            - key_value_pairs: Extracted key-value pairs (if any)
            - metadata: Additional metadata
    """
    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential
    except ImportError:
        raise ImportError(
            "azure-ai-documentintelligence is required. "
            "Install with: pip install azure-ai-documentintelligence"
        )

    endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError(
            "Azure Document Intelligence credentials not provided."
        )

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    logger.info(f"Analyzing document structure: {file_path}")

    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    with open(file_path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-layout",
            body=f,
            content_type="application/octet-stream",
            output_content_format="markdown",
            pages="1-",  # Extract ALL pages (1 to end)
        )

    result = poller.result()

    # Extract structured data
    structured_data = {
        "markdown": result.content,
        "pages": len(result.pages),
        "tables": [],
        "key_value_pairs": [],
        "metadata": {
            "file_name": file_path.name,
            "file_size_mb": file_path.stat().st_size / (1024 * 1024),
            "file_extension": file_path.suffix.lower(),
        }
    }

    # Extract tables if present
    if hasattr(result, 'tables') and result.tables:
        for table in result.tables:
            table_data = {
                "row_count": table.row_count,
                "column_count": table.column_count,
                "cells": []
            }
            if hasattr(table, 'cells'):
                for cell in table.cells:
                    table_data["cells"].append({
                        "row_index": cell.row_index,
                        "column_index": cell.column_index,
                        "content": cell.content,
                        "kind": cell.kind if hasattr(cell, 'kind') else None,
                    })
            structured_data["tables"].append(table_data)

    # Extract key-value pairs if present
    if hasattr(result, 'key_value_pairs') and result.key_value_pairs:
        for kv in result.key_value_pairs:
            if hasattr(kv, 'key') and hasattr(kv, 'value'):
                structured_data["key_value_pairs"].append({
                    "key": kv.key.content if hasattr(kv.key, 'content') else str(kv.key),
                    "value": kv.value.content if hasattr(kv.value, 'content') else str(kv.value),
                })

    logger.info(f"Extracted: {len(structured_data['tables'])} tables, "
                f"{len(structured_data['key_value_pairs'])} key-value pairs")

    return structured_data


def is_azure_document_intelligence_available() -> bool:
    """
    Check if Azure Document Intelligence is properly configured.

    Returns:
        True if endpoint and key are available, False otherwise
    """
    endpoint = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        logger.warning(
            "Azure Document Intelligence not configured. "
            "Set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY"
        )
        return False

    try:
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        return True
    except ImportError:
        logger.warning("azure-ai-documentintelligence package not installed")
        return False


def parse_pdf_via_images(
    pdf_path: str,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    dpi: int = 200
) -> str:
    """
    Parse PDF by converting each page to an image using PyMuPDF and processing with Document Intelligence.

    This approach extracts ALL pages and works better than direct PDF parsing for some documents.
    Uses PyMuPDF (fitz) which is fast and has no external dependencies.

    Args:
        pdf_path: Path to PDF file
        endpoint: Azure Document Intelligence endpoint
        key: Azure Document Intelligence key
        dpi: DPI for image conversion (default 200)

    Returns:
        Concatenated markdown content from all pages
    """
    try:
        import fitz  # PyMuPDF
        from azure.ai.documentintelligence import DocumentIntelligenceClient
        from azure.core.credentials import AzureKeyCredential
        import io
    except ImportError as e:
        raise ImportError(
            f"Required package not installed: {e}. "
            "Install with: pip install pymupdf azure-ai-documentintelligence"
        )

    # Get credentials
    endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
    key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Document Intelligence credentials not provided")

    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    logger.info(f"Converting PDF pages to images with PyMuPDF: {pdf_path}")

    # Open PDF with PyMuPDF
    try:
        pdf_document = fitz.open(str(pdf_path))
        page_count = len(pdf_document)
        logger.info(f"PDF has {page_count} pages")
    except Exception as e:
        logger.error(f"Failed to open PDF with PyMuPDF: {e}")
        raise

    # Initialize Document Intelligence client
    client = DocumentIntelligenceClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key)
    )

    # Process each page
    all_markdown = []

    for page_num in range(page_count):
        logger.info(f"Processing page {page_num + 1}/{page_count} with Document Intelligence...")

        try:
            # Get the page
            page = pdf_document[page_num]

            # Convert page to image (PNG)
            # zoom factor: 2.0 = 200 DPI, 1.0 = 100 DPI
            zoom = dpi / 100.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)

            # Convert pixmap to PNG bytes
            img_bytes = pix.tobytes("png")
            img_byte_arr = io.BytesIO(img_bytes)

            # Analyze image with Document Intelligence
            poller = client.begin_analyze_document(
                model_id="prebuilt-layout",
                body=img_byte_arr,
                content_type="image/png",
                output_content_format="markdown",
            )

            result = poller.result()
            page_markdown = result.content

            all_markdown.append(f"<!-- Page {page_num + 1} -->\n{page_markdown}\n")
            logger.info(f"Page {page_num + 1}: Extracted {len(page_markdown)} characters")

        except Exception as e:
            logger.warning(f"Failed to process page {page_num + 1}: {e}")
            all_markdown.append(f"<!-- Page {page_num + 1}: Extraction failed -->\n")

    # Close the PDF
    pdf_document.close()

    # Combine all pages
    full_markdown = "\n".join(all_markdown)
    logger.info(f"Successfully extracted {len(full_markdown)} characters from {page_count} pages")

    return full_markdown

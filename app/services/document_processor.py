"""Document processing service."""
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import csv
from io import StringIO
import PyPDF2
import pdfplumber
from app.config import get_settings
from app.utils.logger import get_logger
from app.utils.language import detect_language
from app.utils.embeddings import generate_embeddings
from app.models import DocumentChunk, DocumentMetadata

logger = get_logger(__name__)


def chunk_text(
    text: str,
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None
) -> List[str]:
    """
    Split text into chunks.
    
    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in characters
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of text chunks
    """
    settings = get_settings()
    chunk_size = chunk_size or settings.chunk_size
    chunk_overlap = chunk_overlap or settings.chunk_overlap
    
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - chunk_overlap
    
    return chunks


def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF file."""
    try:
        # Try using pdfplumber first (better for complex PDFs)
        with pdfplumber.open(file_content) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        logger.warning(f"pdfplumber extraction failed: {e}, trying PyPDF2")
        
        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(file_content)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            logger.error(f"PDF extraction failed: {e}")
            raise


def extract_text_from_txt(file_content: bytes) -> str:
    """Extract text from TXT file."""
    try:
        return file_content.decode('utf-8')
    except UnicodeDecodeError:
        # Try other encodings
        for encoding in ['latin-1', 'cp1252', 'iso-8859-1']:
            try:
                return file_content.decode(encoding)
            except:
                continue
        raise ValueError("Could not decode text file with any supported encoding")


def extract_text_from_markdown(file_content: bytes) -> str:
    """Extract text from Markdown file."""
    return extract_text_from_txt(file_content)


def extract_text_from_json(file_content: bytes) -> str:
    """Extract text from JSON file."""
    try:
        data = json.loads(file_content.decode('utf-8'))
        
        # Convert JSON to readable text
        def json_to_text(obj, indent=0):
            text = ""
            if isinstance(obj, dict):
                for key, value in obj.items():
                    text += "  " * indent + f"{key}: "
                    if isinstance(value, (dict, list)):
                        text += "\n" + json_to_text(value, indent + 1)
                    else:
                        text += str(value) + "\n"
            elif isinstance(obj, list):
                for item in obj:
                    text += json_to_text(item, indent)
            else:
                text += str(obj) + "\n"
            return text
        
        return json_to_text(data)
    except Exception as e:
        logger.error(f"JSON extraction failed: {e}")
        raise


def extract_text_from_csv(file_content: bytes) -> str:
    """Extract text from CSV file."""
    try:
        text_content = file_content.decode('utf-8')
        reader = csv.DictReader(StringIO(text_content))
        
        text = ""
        for row in reader:
            for key, value in row.items():
                text += f"{key}: {value}\n"
            text += "\n"
        
        return text
    except Exception as e:
        logger.error(f"CSV extraction failed: {e}")
        raise


def extract_text(file_content: bytes, file_type: str) -> str:
    """
    Extract text from file based on file type.
    
    Args:
        file_content: File content as bytes
        file_type: Type of file (pdf, txt, md, json, csv)
        
    Returns:
        Extracted text
    """
    file_type = file_type.lower()
    
    if file_type == "pdf":
        return extract_text_from_pdf(file_content)
    elif file_type == "txt":
        return extract_text_from_txt(file_content)
    elif file_type == "md":
        return extract_text_from_markdown(file_content)
    elif file_type == "json":
        return extract_text_from_json(file_content)
    elif file_type == "csv":
        return extract_text_from_csv(file_content)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")


def process_document(
    file_name: str,
    file_type: str,
    file_content: bytes,
    language: Optional[str] = None
) -> List[DocumentChunk]:
    """
    Process a document and create chunks with embeddings.
    
    Args:
        file_name: Name of the file
        file_type: Type of file
        file_content: File content as bytes
        language: Optional language code
        
    Returns:
        List of document chunks
    """
    logger.info(f"Processing document: {file_name}")
    
    # Extract text
    text = extract_text(file_content, file_type)
    logger.info(f"Extracted {len(text)} characters from {file_name}")
    
    # Detect language if not provided
    if not language:
        language, confidence = detect_language(text)
        logger.info(f"Detected language: {language} (confidence: {confidence:.2f})")
    
    # Chunk text
    chunks = chunk_text(text)
    logger.info(f"Created {len(chunks)} chunks from {file_name}")
    
    # Generate embeddings
    embeddings = generate_embeddings(chunks)
    
    # Create document chunks
    document_chunks = []
    for i, (chunk_content, embedding) in enumerate(zip(chunks, embeddings)):
        chunk_id = f"{file_name}_{i}"

        metadata = DocumentMetadata(
            source=file_name,
            file_type=file_type,
            language=language,
            chunk_index=i,
            total_chunks=len(chunks),
            timestamp=datetime.utcnow(),
            original_filename=file_name
        )

        doc_chunk = DocumentChunk(
            id=chunk_id,
            content=chunk_content,
            metadata=metadata,
            embedding=embedding
        )

        document_chunks.append(doc_chunk)
    
    logger.info(f"Created {len(document_chunks)} document chunks with embeddings")
    return document_chunks


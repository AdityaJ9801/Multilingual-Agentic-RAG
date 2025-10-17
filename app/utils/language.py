"""Language detection and processing utilities."""
from typing import Tuple, Optional
from langdetect import detect, detect_langs, LangDetectException
from app.config import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Language code mappings
LANGUAGE_NAMES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "zh": "Chinese",
    "ar": "Arabic",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
}


def detect_language(text: str) -> Tuple[str, float]:
    """
    Detect the language of the given text.
    
    Args:
        text: Text to detect language for
        
    Returns:
        Tuple of (language_code, confidence)
    """
    settings = get_settings()
    
    if not text or len(text.strip()) < 3:
        return settings.default_language, 0.0
    
    try:
        # Try to detect language
        detected_lang = detect(text)
        
        # Get confidence scores
        probabilities = detect_langs(text)
        confidence = 0.0
        
        for prob in probabilities:
            if prob.lang == detected_lang:
                confidence = prob.prob
                break
        
        # Check if detected language is supported
        if detected_lang in settings.supported_languages:
            if confidence >= settings.language_detection_confidence_threshold:
                logger.info(
                    f"Detected language: {detected_lang} (confidence: {confidence:.2f})"
                )
                return detected_lang, confidence
        
        # Fall back to default language if confidence is low or language not supported
        logger.warning(
            f"Language detection confidence too low ({confidence:.2f}) or language not supported. "
            f"Using default: {settings.default_language}"
        )
        return settings.default_language, confidence
        
    except LangDetectException as e:
        logger.warning(f"Language detection failed: {e}. Using default language.")
        return settings.default_language, 0.0
    except Exception as e:
        logger.error(f"Unexpected error in language detection: {e}")
        return settings.default_language, 0.0


def get_language_name(language_code: str) -> str:
    """Get the full name of a language from its code."""
    return LANGUAGE_NAMES.get(language_code, language_code.upper())


def is_language_supported(language_code: str) -> bool:
    """Check if a language is supported."""
    settings = get_settings()
    return language_code in settings.supported_languages


def validate_language(language_code: Optional[str]) -> str:
    """
    Validate and return a language code.
    
    Args:
        language_code: Language code to validate
        
    Returns:
        Valid language code
        
    Raises:
        ValueError: If language is not supported
    """
    settings = get_settings()
    
    if language_code is None:
        return settings.default_language
    
    if not is_language_supported(language_code):
        raise ValueError(
            f"Language '{language_code}' is not supported. "
            f"Supported languages: {', '.join(settings.supported_languages)}"
        )
    
    return language_code


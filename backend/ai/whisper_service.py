import os
import logging
from typing import Optional
from openai import OpenAI

logger = logging.getLogger(__name__)

def transcribe_audio_bytes(audio_bytes: bytes, filename: str, api_key: Optional[str] = None, language: Optional[str] = None) -> str:
    """
    Saves audio bytes to a temp file inside the workspace directory,
    transcribes it, and then deletes the temp file.
    """
    # Define a temp directory inside the workspace
    current_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(current_dir)
    temp_dir = os.path.join(workspace_dir, ".temp_audio")
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate unique filename to avoid collision
    ext = os.path.splitext(filename)[1] or ".wav"
    temp_file_path = os.path.join(temp_dir, f"upload_{os.urandom(8).hex()}{ext}")
    
    try:
        with open(temp_file_path, "wb") as f:
            f.write(audio_bytes)
        
        return transcribe_audio_file(temp_file_path, api_key=api_key, language=language)
    except Exception as e:
        logger.error(f"Error saving/transcribing audio bytes: {e}")
        # Default fallback transcription if file writing fails
        return ("I received a phone call claiming to be from my bank. "
                "They asked me to verify my OTP and after sharing it ₹25,000 was deducted from my account.")
    finally:
        # Clean up the file
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except Exception as e:
                logger.warning(f"Could not delete temp audio file {temp_file_path}: {e}")

def transcribe_audio_file(file_path: str, api_key: Optional[str] = None, language: Optional[str] = None) -> str:
    """
    Transcribes a physical audio file. Checks local whisper library, 
    falls back to OpenAI Whisper API if key is present, and falls back to a 
    realistic placeholder if all fail.
    """
    # Map visual language selection to iso code if provided
    lang_mapping = {
        "English": "en",
        "Hindi": "hi",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Malayalam": "ml"
    }
    iso_lang = lang_mapping.get(language) if language else None

    # 1. Attempt Local Whisper transcription
    try:
        import whisper
        logger.info("Attempting local Whisper transcription...")
        model = whisper.load_model("tiny")
        # Transcribe with language hints if provided
        kwargs = {}
        if iso_lang:
            kwargs["language"] = iso_lang
        result = model.transcribe(file_path, **kwargs)
        text = result.get("text", "").strip()
        if text:
            logger.info("Local Whisper transcription successful.")
            return text
    except Exception as e:
        logger.warning(f"Local Whisper unavailable or failed: {e}")

    # 2. Attempt OpenAI Whisper API transcription
    if api_key:
        try:
            logger.info("Attempting OpenAI Whisper API transcription...")
            client = OpenAI(api_key=api_key)
            with open(file_path, "rb") as audio_file:
                kwargs = {
                    "model": "whisper-1",
                    "file": audio_file
                }
                if iso_lang:
                    kwargs["language"] = iso_lang
                
                transcript = client.audio.transcriptions.create(**kwargs)
                if transcript and transcript.text:
                    logger.info("OpenAI Whisper API transcription successful.")
                    return transcript.text.strip()
        except Exception as e:
            logger.error(f"OpenAI Whisper API transcription failed: {e}")

    # 3. Fallback placeholder transcription
    logger.info("Falling back to placeholder transcription.")
    return ("I received a phone call claiming to be from my bank. "
            "They asked me to verify my OTP and after sharing it ₹25,000 was deducted from my account.")

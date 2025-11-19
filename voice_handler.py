# ============================================================================
# File: voice_handler.py
"""Voice input handling using Google Speech Recognition."""

import streamlit as st
import speech_recognition as sr
from typing import Optional


def initialize_recognizer():
    """Initialize speech recognizer."""
    return sr.Recognizer()


def record_audio(duration: int = 5) -> Optional[sr.AudioData]:
    """
    Record audio from microphone.
    
    :param duration: Recording duration in seconds
    :return: AudioData object or None
    """
    recognizer = initialize_recognizer()
    
    try:
        with sr.Microphone() as source:
            st.info("🎤 Listening... Please speak now.")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            return audio
    except sr.WaitTimeoutError:
        st.warning("⏱️ No speech detected. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ Error recording audio: {str(e)}")
        return None


def transcribe_audio(audio: sr.AudioData) -> Optional[str]:
    """
    Transcribe audio to text using Google Speech Recognition.
    
    :param audio: AudioData object
    :return: Transcribed text or None
    """
    recognizer = initialize_recognizer()
    
    try:
        st.info("🔄 Transcribing...")
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        st.warning("❌ Could not understand audio. Please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"❌ Speech recognition service error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"❌ Error transcribing audio: {str(e)}")
        return None


def get_voice_input(duration: int = 10) -> Optional[str]:
    """
    Complete voice input flow: record and transcribe.
    
    :param duration: Recording duration in seconds
    :return: Transcribed text or None
    """
    audio = record_audio(duration)
    if audio:
        return transcribe_audio(audio)
    return None


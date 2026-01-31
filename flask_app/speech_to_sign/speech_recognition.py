import speech_recognition as sr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import re

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        
        # Try to initialize microphone (optional - may fail if PyAudio not installed)
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
        except (AttributeError, OSError) as e:
            print(f"Note: Microphone not available ({e}). Speech from microphone will be disabled.")
            print("The app will still work with text input and browser-based speech recognition.")
    
    def recognize_speech(self, duration=5):
        """Recognize speech from microphone"""
        if self.microphone is None:
            return "Microphone not available. Please use text input or browser speech recognition."
        
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            # Try Google Speech Recognition first
            try:
                text = self.recognizer.recognize_google(audio)
                return text.lower()
            except sr.RequestError:
                # Fallback to Sphinx (offline)
                text = self.recognizer.recognize_sphinx(audio)
                return text.lower()
                
        except sr.WaitTimeoutError:
            return "No speech detected"
        except sr.UnknownValueError:
            return "Could not understand audio"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def recognize_from_file(self, audio_file):
        """Recognize speech from audio file"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            text = self.recognizer.recognize_google(audio)
            return text.lower()
        except Exception as e:
            return f"Error: {str(e)}"

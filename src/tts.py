import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "site-packages"))

from gtts import gTTS, lang

# Use gTTS to generate text-to-speech for the given word and language pair
def generate_tts(text, lang=''):
    return gTTS(text, lang=lang)

# Return list of supported TTS languages
def get_supported_langs(): return lang.tts_langs()
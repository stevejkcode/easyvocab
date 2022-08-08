import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "site-packages"))

from gtts import gTTS

# Use gTTS to generate text-to-speech for the given word and language pair
def generate_tts(text, lang=''):
    return gTTS(text, lang=lang)
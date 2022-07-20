import os
import sys

name = 'prettify-nord-basic-fl'

with open(os.path.join(os.path.dirname(__file__), './afmt.html'), 'r') as html:
    afmt = html.read()

with open(os.path.join(os.path.dirname(__file__), './qfmt.html'), 'r') as html:
    qfmt = html.read()

with open(os.path.join(os.path.dirname(__file__), './main.css'), 'r') as file:
    css = file.read()

# fields
    # foreign language word
    # your language definition
    # foreign language explanation
    # your language explanation
fields = [
    'ForeignLanguageWord',
    'ForeignLanguageExplanation',
    'ForeignLanguagePronunciation'
    'YourLanguageDefinition',
    'YourLanguageExplanation'
]

templates = [
    {
        'name': 'forward-template',
        'afmt': afmt,
        'qfmt': qfmt
    }
]
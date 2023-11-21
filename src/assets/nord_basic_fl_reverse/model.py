import os
import sys

name = 'Prettify Vocabulary Card (Reverse)'

with open(os.path.join(os.path.dirname(__file__), './card1_afmt.html'), 'r') as html:
    card1_afmt = html.read()

with open(os.path.join(os.path.dirname(__file__), './card1_qfmt.html'), 'r') as html:
    card1_qfmt = html.read()

with open(os.path.join(os.path.dirname(__file__), './card2_afmt.html'), 'r') as html:
    card2_afmt = html.read()

with open(os.path.join(os.path.dirname(__file__), './card2_qfmt.html'), 'r') as html:
    card2_qfmt = html.read()

with open(os.path.join(os.path.dirname(__file__), './main.css'), 'r') as file:
    css = file.read()

fields = [
    'ForeignLanguageWord',
    'YourLanguageDefinition',
    'YourLanguageImage',
    'ForeignLanguagePronunciation',
    'ForeignLanguageExplanationWordType_1',
    'ForeignLanguageExplanationDetails_1',
    'ForeignLanguageExplanationWordType_2',
    'ForeignLanguageExplanationDetails_2',
    'ForeignLanguageExplanationWordType_3',
    'ForeignLanguageExplanationDetails_3',
    'YourLanguageExplanationWordType_1',
    'YourLanguageExplanationDetails_1',
    'YourLanguageExplanationWordType_2',
    'YourLanguageExplanationDetails_2',
    'YourLanguageExplanationWordType_3',
    'YourLanguageExplanationDetails_3',
]

templates = [
    {
        'name': 'Vocabulary Card',
        'afmt': card1_afmt,
        'qfmt': card1_qfmt
    },
    {
        'name': 'Vocabulary Card (Reverse)',
        'afmt': card2_afmt,
        'qfmt': card2_qfmt
    }
]
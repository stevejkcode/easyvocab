import os
import sys

name = 'prettify-nord-basic-fl_reverse'

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

fields = ['Front', 'Back']

templates = [
    {
        'name': 'forward-template',
        'afmt': card1_afmt,
        'qfmt': card1_qfmt
    },
    {
        'name': 'reverse-template',
        'afmt': card2_afmt,
        'qfmt': card2_qfmt
    }
]
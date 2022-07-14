# import anki

import os
import sys

from anki.decks import DeckId
from anki.collection import Collection

from aqt import mw

from .translate import translate_word

sys.path.append(os.path.join(os.path.dirname(__file__), "site-packages"))


def get_model_id(col, model_name):
    return col.models.id_for_name(model_name)

def get_deck_id(col, deck_name):
    return col.decks.id_for_name(deck_name)

# Find potential duplicate cards 
# Note that deck can be '*' to find duplicates across all decks
def find_dupes(col, deck, fieldname, value):
    cards = col.find_cards(f'\"deck:{deck}\" \"{fieldname}:{value}\"')
    return cards


def generate_cards(collection, deck, text, options):
    text = text.split('\n')

    # default translations number
    translations = 2

    # Get the source and destination language from the options if present
    if options and options.get('language'):
        dest = options.get('language').get('dest')
        src  = options.get('language').get('src')

    # Get the number of translations from the options if present
    if options and options.get('translations'):
        translations = options.get('translations')

    if not collection or type(collection) is str:
        # Open collection
        collection = Collection(collection)

    # Retrieve deck id
    deck_id = get_deck_id(collection, deck.name) # TODO: Replace this with actual deck name param

    # Retrieve note model id
    model_id = get_model_id(collection, 'Basic')

    for word in text:
    # For each word
        # Remove any random whitespace or crud from the question
        question = word.strip()

        ## Filter for dupes
        # Find duplicate cards
        dupes = find_dupes(collection, deck.name, 'Front', question)

        # If there are any dupes, continue rather than adding this card to the deck 
        if len(dupes) > 0: continue

        print(f'translating {question}')

        # Translate
        answer = ', '.join(translate_word(question, translations, src = src, dest = dest))

        # Create card with original text + definition
        note = collection.new_note(model_id)
        note.fields = [question, answer]

        # Add card to deck
        collection.add_note(note, deck_id)

        # Generate a reverse card if reverse cards is enabled
        if options.get('reverse') or options.get('reverse') == 'true':
            rnote = collection.new_note(model_id)
            rnote.fields = [answer, question]   # flip the answer and question 
            collection.add_note(rnote, deck_id)

    # collection.close()


## __main__
# main()

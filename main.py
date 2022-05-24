# import anki

import os

from anki.collection import Collection
from anki.decks import DeckId

from translate import translate_word


## Env variables for process params
DECK       = os.environ.get('ANKI_DECK',       'French') # TODO: Update this with the real deck name
COLLECTION = os.environ.get('ANKI_COLLECTION', '~/.local/share/User/collection.anki2')


def get_model_id(col, model_name):
    return col.models.id_for_name(model_name)

def get_deck_id(col, deck_name):
    return col.decks.id_for_name(deck_name)

# Find potential duplicate cards 
# Note that deck can be '*' to find duplicates across all decks
def find_dupes(col, deck, fieldname, value):
    cards = col.find_cards(f'\"deck:{deck}\" \"{fieldname}:{value}\"')
    return cards

def main():
    # Open collection
    col = Collection(COLLECTION)

    # Retrieve deck id
    deck_id = get_deck_id(col, DECK) # TODO: Replace this with actual deck name param

    # Retrieve note model id
    model_id = get_model_id(col, 'Basic')

    # # Open words file
    with open("./words.txt", "r") as words:
        for word in words:
        # For each word
            # Remove any random whitespace or crud from the question
            question = word.strip()

            ## Filter for dupes
            # Find duplicate cards
            dupes = find_dupes(col, DECK, 'Front', question)

            # If there are any dupes, continue rather than adding this card to the deck 
            if len(dupes) > 0: continue

            print(f'translating {question}')

            # Translate
            answer = ', '.join(translate_word(question))

            # Create card with original text + definition
            note = col.new_note(model_id)
            note.fields = [question, answer]

            # Add card to deck
            col.add_note(note, deck_id)

    col.close()


## __main__
main()

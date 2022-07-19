# import anki

import os
import sys

from anki.decks import DeckId
from anki.collection import Collection

from aqt import mw

from .translate import translate_word
from .assets import build, nord_basic_fl

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

# Create a card with the given question and answer
def create_forward_card(collection, model_id, deck_id, question, answer):
    # Create card with original text + definition
    note = collection.new_note(model_id)
    note.fields = [question, answer]

    # Add card to deck
    collection.add_note(note, deck_id)
    return

# Create a reverse card with the question and answer flipped
def create_reverse_card(collection, model_id, deck_id, question, answer):
    return create_forward_card(collection, model_id, deck_id, answer, question)

# Process an individual word, creating cards for it as needed
def process_word(collection, deck, word, i, count, translations, reverse, src, dest, deck_id, model_id, progress_f):
    # Remove any random whitespace or crud from the question
    question = word.strip()

    # Reject any cards with blank text
    if word == '':
        return

    ## Filter for dupes
    # Find duplicate cards
    forward_dupes = find_dupes(collection, deck.name, 'Front', question)
    reverse_dupes = find_dupes(collection, deck.name, 'Back', question)

    # If there are duplicate cards, continue rather than adding this card to the deck 
    if len(forward_dupes) > 0 and len(reverse_dupes) > 0: return mw.taskman.run_on_main(lambda: progress_f(word, i, count))

    # If reverse is false, skip the process if there are forward duplicate cards
    if len(forward_dupes) > 0 and not reverse: return mw.taskman.run_on_main(lambda: progress_f(word, i, count))

    print(f'translating {question}')

    # Translate
    translation = translate_word(question, translations, src, dest)
    answer = ', '.join(translation)

    # Create forward card if necessary
    if len(forward_dupes) == 0: create_forward_card(collection, model_id, deck_id, question, answer)

    # Create reverse card if necessary
    if reverse and len(reverse_dupes) == 0: create_reverse_card(collection, model_id, deck_id, question, answer)

    return mw.taskman.run_on_main(lambda: progress_f(word, i, count))

# Outer function for running the card generation process
# Note that this is run inside a background process in anki (hence the use of currying)
def process_words(collection, deck, words, translations, reverse, src, dest, deck_id, model_id, progress_f):
    def _f():
        count = len(words)
        i = 0

        for word in words:
            process_word(collection, deck, word, i + 1, count, translations, reverse, src, dest, deck_id, model_id, progress_f)
            i += 1

    return _f

# Simple callback function for closing out the overall background generation routine
def finish_f(main_dialog, progress_dialog):
    def _f(future):
        print(f'finished with result: {future.result()}')
        progress_dialog.close()
        main_dialog.close()

    return _f


def generate_cards(collection, deck, text, options, main_dialog, progress_dialog):
    # Build the note types if needed
    build.build_asset(nord_basic_fl.model)

    text = text.split('\n')

    reverse = False

    # default translations number
    translations = 2

    # Get the source and destination language from the options if present
    if options and options.get('language'):
        dest = options.get('language').get('dest')
        src  = options.get('language').get('src')

    # Get the number of translations from the options if present
    if options and options.get('translations'):
        translations = options.get('translations')

    if options and options.get('reverse'):
        reverse = options.get('reverse')

    if not collection or type(collection) is str:
        # Open collection
        collection = Collection(collection)

    # Retrieve deck id
    deck_id = get_deck_id(collection, deck.name) # TODO: Replace this with actual deck name param

    # Retrieve note model id
    model_id = get_model_id(collection, nord_basic_fl.model.name)

    progress_f = progress_dialog.ui.updateProgress

    # Trigger the card generation process in the background
    # finish_f will be called when the process is finished
    mw.taskman.run_in_background(process_words(collection, deck, text, translations, reverse, src, dest, deck_id, model_id, progress_f),
                                finish_f(main_dialog, progress_dialog))


## __main__
# main()

# import anki

import os
import sys

from anki.decks import DeckId
from anki.collection import Collection
from anki.media import media_paths_from_col_path

from anki.notetypes_pb2 import ChangeNotetypeRequest

from aqt import mw

from .translate import translate_word
from .assets import build, nord_basic_fl, nord_basic_fl_reverse
from .tts import generate_tts
from .hash import get_media_hash

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "site-packages"))


def get_model_id(col, model_name):
    return col.models.id_for_name(model_name)

def get_deck_id(col, deck_name):
    return col.decks.id_for_name(deck_name)

# Find potential duplicate cards
# Note that deck can be '*' to find duplicates across all decks
def find_dupes(col, deck, fieldname, value):
    cards = col.find_notes(f'\"deck:{deck}\" \"{fieldname}:{value}\"')
    return cards

# Create cards for the notetype with the given question and answer
def create_cards(collection, model_id, deck_id, card):
    # Create card with original text + definition
    note = collection.new_note(model_id)
    note.fields = [
        card['ForeignLanguageWord'],
        card['YourLanguageDefinition'],
        card['ForeignLanguagePronunciation'],
        card['ForeignLanguageExplanationWordType_1'],
        card['ForeignLanguageExplanationDetails_1'],
        card['ForeignLanguageExplanationWordType_2'],
        card['ForeignLanguageExplanationDetails_2'],
        card['ForeignLanguageExplanationWordType_3'],
        card['ForeignLanguageExplanationDetails_3'],
        card['YourLanguageExplanationWordType_1'],
        card['YourLanguageExplanationDetails_1'],
        card['YourLanguageExplanationWordType_2'],
        card['YourLanguageExplanationDetails_2'],
        card['YourLanguageExplanationWordType_3'],
        card['YourLanguageExplanationDetails_3']
    ]

    # Add card to deck
    collection.add_note(note, deck_id)
    return

# Update the notetype of an existing basic card to a reverse card
# This will add a reverse card to the existing forward card without
# wiping out the stats of the forward card or needing to recreate it
def update_basic_to_reverse(collection, note_id):
    old_model = collection.models.by_name(nord_basic_fl.model.name)
    new_model = collection.models.by_name(nord_basic_fl_reverse.model.name)
    
    request = ChangeNotetypeRequest()
    request.ParseFromString(collection.models.change_notetype_info(old_notetype_id=old_model['id'], new_notetype_id=new_model['id']).input.SerializeToString())
    request.note_ids.extend([ note_id ])
    collection.models.change_notetype_of_notes(request)

# Process an individual word, creating cards for it as needed
def process_word(collection, deck, word, i, count, num_translations, reverse, src, dest, deck_id, model_id, progress_f):
    # Remove any random whitespace or crud from the question
    question = word.strip()

    # Reject any cards with blank text
    if word == '':
        return

    ## Filter for dupes
    # Find duplicate cards
    forward_dupes = find_dupes(collection, deck.name, 'ForeignLanguageWord', question)
    reverse_dupes = find_dupes(collection, deck.name, 'YourLanguageDefinition', question)

    # If there are duplicate cards, continue rather than adding this card to the deck 
    if len(forward_dupes) > 0 and len(reverse_dupes) > 0: return mw.taskman.run_on_main(lambda: progress_f(word, i, count))

    # If reverse is false, skip the process if there are forward duplicate cards
    if len(forward_dupes) > 0 and not reverse: return mw.taskman.run_on_main(lambda: progress_f(word, i, count))

    # If reverse is enabled and a forward card already exists, change the notetype to reverse
    # to automatically generate a matching reverse card 
    if len(forward_dupes) > 0 and reverse:
        update_basic_to_reverse(collection, forward_dupes[0])
        return mw.taskman.run_on_main(lambda: progress_f(word, i, count))

    print(f'translating {question}')

    # Translate
    translations = translate_word(question, num_translations, src, dest)

    translation = translations[0]
    answer = ', '.join(translation)

    card = {
        'ForeignLanguageWord': question,
        'YourLanguageDefinition': answer,
        'ForeignLanguagePronunciation': '',
        'ForeignLanguageExplanationWordType_1': translations[1],
        'ForeignLanguageExplanationDetails_1': translations[2],
        'ForeignLanguageExplanationWordType_2': translations[3],
        'ForeignLanguageExplanationDetails_2': translations[4],
        'ForeignLanguageExplanationWordType_3': translations[5],
        'ForeignLanguageExplanationDetails_3': translations[6],
        'YourLanguageExplanationWordType_1': translations[7],
        'YourLanguageExplanationDetails_1': translations[8],
        'YourLanguageExplanationWordType_2': translations[9],
        'YourLanguageExplanationDetails_2': translations[10],
        'YourLanguageExplanationWordType_3': translations[11],
        'YourLanguageExplanationDetails_3': translations[12]
    }

    # Generate text-to-speech
    # create media filename
    media_hash = get_media_hash(question)
    media_filename = f'{media_hash}.mp3'

    # get the media location
    [ media_dir, _ ] = media_paths_from_col_path(collection.path)

    # call tts to create the audio
    tts = generate_tts(question, lang=src)

    # save generated tts to the media dir
    media_full_path = os.path.join(media_dir, media_filename)
    tts.save(media_full_path)

    # place media in the resulting card
    card['ForeignLanguagePronunciation'] = f'[sound:{media_filename}]'

    create_cards(collection, model_id, deck_id, card)

    # Create forward card if necessary
    # if len(forward_dupes) == 0: create_forward_card(collection, model_id, deck_id, question, answer)

    # Create reverse card if necessary
    # if reverse and len(reverse_dupes) == 0: create_reverse_card(collection, model_id, deck_id, question, answer)

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
    build.build_asset(nord_basic_fl_reverse.model)

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
    deck_id = get_deck_id(collection, deck.name)

    # Forward and reverse model version
    # Retrieve note model id
    if reverse:
        model_id = get_model_id(collection, nord_basic_fl_reverse.model.name)
    else:
        model_id = get_model_id(collection, nord_basic_fl.model.name)    
                
    progress_f = progress_dialog.ui.updateProgress

    # Trigger the card generation process in the background
    # finish_f will be called when the process is finished
    mw.taskman.run_in_background(process_words(collection, deck, text, translations, reverse, src, dest, deck_id, model_id, progress_f),
                                finish_f(main_dialog, progress_dialog))


## __main__
# main()

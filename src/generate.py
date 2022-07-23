# import anki

import os

from anki.decks import DeckId
from anki.media import media_paths_from_col_path

from aqt import mw

from . import assets, collection, hash, translate, tts, util

# Process an individual word, creating cards for it as needed
def process_word(col, deck, word, options, progress):
    # default values
    reverse = False
    num_translations = 2

    # Get the source and destination language from the options if present
    if options and options.get('language'):
        dest = options.get('language').get('dest')
        src  = options.get('language').get('src')

    # Get the number of translations from the options if present
    if options and options.get('num_translations'):
        num_translations = options.get('num_translations')

    if options and options.get('reverse'):
        reverse = options.get('reverse')

    if options and options.get('deck'):
        deck_id = options.get('deck').get('id')
    
    if options and options.get('model'):
        model_id = options.get('model').get('id')

    # Remove any random whitespace or crud from the question
    question = word.strip()

    # Reject any cards with blank text
    if word == '':
        return

    ## Filter for dupes
    # Find duplicate cards
    forward_dupes = collection.find_dupes(col, deck.name, 'ForeignLanguageWord', question)
    reverse_dupes = collection.find_dupes(col, deck.name, 'YourLanguageDefinition', question)

    # If there are duplicate cards, continue rather than adding this card to the deck 
    if len(forward_dupes) > 0 and len(reverse_dupes) > 0: return mw.taskman.run_on_main(progress)

    # If reverse is false, skip the process if there are forward duplicate cards
    if len(forward_dupes) > 0 and not reverse: return mw.taskman.run_on_main(progress)

    # If reverse is enabled and a forward card already exists, change the notetype to reverse
    # to automatically generate a matching reverse card 
    if len(forward_dupes) > 0 and reverse:
        collection.update_basic_to_reverse(col, forward_dupes[0])
        return mw.taskman.run_on_main(progress)

    print(f'translating {question}')

    # Translate
    translations = translate.translate_word(question, num_translations, src, dest)

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
    # Create media filename
    media_hash = hash.get_media_hash(question)
    media_filename = f'{media_hash}.mp3'

    # Get the media location
    [ media_dir, _ ] = media_paths_from_col_path(col.path)

    # Call tts to create the audio
    speach = tts.generate_tts(question, lang=src)

    # Save generated tts to the media dir
    media_full_path = os.path.join(media_dir, media_filename)
    speach.save(media_full_path)

    # Place media in the resulting card
    card['ForeignLanguagePronunciation'] = f'[sound:{media_filename}]'

    # Generate final cards
    collection.create_cards(col, model_id, deck_id, card)

    return mw.taskman.run_on_main(progress)

# Outer function for running the card generation process
# Note that this is run inside a background process in anki
def process_words(col, deck, words, options, progress):
    count = len(words)
    i = 0

    for word in words:
        process_word(col, deck, word, options, progress(word, i + 1, count))
        i += 1

# Simple callback function for closing out the overall background generation routine
def finish(dialog):
    def wrap(future):
        print(f'finished with result: {future.result()}')
        dialog['progress'].close()
        dialog['main'].close()
    return wrap


def generate_cards(col, deck, text, options, dialog):
    # Build the note types if needed
    assets.build.build_asset(assets.nord_basic_fl.model)
    assets.build.build_asset(assets.nord_basic_fl_reverse.model)

    text = text.split('\n')    

    # Init collection handle
    col = collection.init_handle(col)
    
    # Retrieve deck id
    deck_id = collection.get_deck_id(col, deck.name)

    # Get model name based on reverse option
    if options.get('reverse'):
        model_name = assets.nord_basic_fl_reverse.model.name
    else:
        model_name = assets.nord_basic_fl.model.name

    # Forward and reverse model version
    # Retrieve note model id
    model_id = collection.get_model_id(col, model_name)

    options['deck']  = { 'name': deck.name,  'id': deck_id }
    options['model'] = { 'name': model_name, 'id': model_id }
                
    progress = util.wrap_nonary(dialog['progress'].ui.updateProgress)

    # Trigger the card generation process in the background
    # The finish handler will be called when the process is finished
    mw.taskman.run_in_background(util.wrap_nonary(process_words)(col, deck, text, options, progress),
                                finish(dialog))

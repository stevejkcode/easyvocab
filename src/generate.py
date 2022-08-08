import os

from anki.media import media_paths_from_col_path

from PyQt5 import QtWidgets
from aqt import mw

from threading import Event

from . import assets, collection, hash, translate, tts, util


# Process and save the tts if possible
def process_tts(col, question, src, card):
    # Generate text-to-speech
    # Create media filename
    media_hash = hash.get_media_hash(question)
    media_filename = f'{media_hash}.mp3'

    # Get the media location
    [ media_dir, _ ] = media_paths_from_col_path(col.path)

    # Autodetect the source lane if not specified
    if src is None or src == '':
        detect = translate.detect_lang(question)
        src    = detect['lang']

    # Call tts to create the audio
    speach = tts.generate_tts(question, lang=src)

    # Save generated tts to the media dir
    media_full_path = os.path.join(media_dir, media_filename)
    speach.save(media_full_path)

    # Place media in the resulting card
    card['ForeignLanguagePronunciation'] = f'[sound:{media_filename}]'

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
    dupes = collection.find_dupes(col, deck.name, 'ForeignLanguageWord', question)

    # Handle duplicate notes / cards
    if len(dupes) > 0:
        dupe = dupes[0]

        # Retrieve note and notetype information
        note     = col.get_note(dupe)
        notetype = note.note_type()

        # If reverse cards are enabled and note type is forward only, update the notetype to generate a reverse card
        if notetype['name'] == assets.nord_basic_fl.model.name and reverse:
            collection.update_basic_to_reverse(col, dupe)
            return mw.taskman.run_on_main(progress)
        
        # Otherwise, skip creating this card because one already exists in this deck
        return mw.taskman.run_on_main(progress)

    # print(f'translating {question}')

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

    if options and options.get('tts'):
        # Attempt to generate a tts, skipping if there is a problem with the generation
        try:
            process_tts(col, question, src, card)
        except: print(f'Warning - failed to generate tts for {question}')

    # Generate final cards
    collection.create_cards(col, model_id, deck_id, card)

    mw.taskman.run_on_main(progress)
    return True

# Outer function for running the card generation process
# Note that this is run inside a background process in anki
def process_words(col, deck, words, options, progress, dialogs, event):
    total = len(words)

    i = 0
    translated = 0

    for word in words:
        # Check to see if the process is cancelled
        if event.is_set():
            # If event is set, the task has been cancelled so we need to return to terminate the process
            return
        
        # Otherwise, we can continue processing the words
        if process_word(col, deck, word, options, progress(word, i + 1, total)): translated += 1
        i += 1
    
    def update():
        dialogs['progress'].ui.textBrowser.append('\n')
        dialogs['progress'].ui.textBrowser.append(f'Generated {translated} cards.')
    
    mw.taskman.run_on_main(update)

def finish(dialogs, col):
    def wrap():
        # Save and flush any outstanding db changes in case the process gets interrupted
        collection.save(col)

        dialogs['progress'].close()
        dialogs['main'].close()

        # Refresh the deck browser so any newly generated cards / decks will appear
        mw.deckBrowser.refresh()

        return
    
    return wrap

# Cancel running card generation and close out UI elements
def cancel(dialogs, future, event):
    def wrap():
        # Cancel the future to stop card generation
        future.cancel()

        # Use the event to signal cancellation if the task is already running
        # (ThreadPoolExecutor cannot directly cancel an already running task)
        event.set()

        # Close UI elements, return user to previous view
        dialogs['progress'].close()
        dialogs['main'].close()

    return wrap

# Simple callback function for closing out the overall background generation routine
# wires buttons in the progress dialog so 
def wire_buttons(dialogs, col):
    def wrap(future):
        dialogs['progress'].ui.buttonBox.button(QtWidgets.QDialogButtonBox.StandardButton.Ok).setDisabled(False)
        dialogs['progress'].ui.buttonBox.accepted.connect(finish(dialogs, col))

    return wrap


# Main card generation process
def generate_cards(col, deck, text, options, dialogs):
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

    # Retrieve note model id
    model_id = collection.get_model_id(col, model_name)

    options['deck']  = { 'name': deck.name,  'id': deck_id }
    options['model'] = { 'name': model_name, 'id': model_id }
                
    progress = util.wrap_nonary(dialogs['progress'].ui.updateProgress)

    event = Event()

    # Trigger the card generation process in the background
    # The finish handler will be called when the process is finished
    future = mw.taskman.run_in_background(util.wrap_nonary(process_words)(col, deck, text, options, progress, dialogs, event),
                                wire_buttons(dialogs, col))

    # Set up cancel button to cancel card generation
    dialogs['progress'].ui.buttonBox.rejected.connect(cancel(dialogs, future, event))

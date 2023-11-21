from anki.collection import Collection
from anki.notetypes_pb2 import ChangeNotetypeRequest
from anki.buildinfo import version

# Internal imports
from .assets import nord_basic_fl, nord_basic_fl_reverse

MIN_VERSION="2.1.50"

# Functions for interacting with anki collections

# Queries

# Retrieve model id
def get_model_id(col: Collection, name: str) -> str:
    return col.models.id_for_name(name)

# Retrieve deck id
def get_deck_id(col: Collection, name: str) -> str:
    return col.decks.id_for_name(name)

# Find potential duplicate cards
# Note that deck can be '*' to find duplicates across all decks
def find_dupes(col: Collection, deck: object, fieldname: str, value: str):
    cards = col.find_notes(f'\"deck:{deck}\" \"{fieldname}:{value}\"')
    return cards

# Create cards for the notetype with the given question and answer
def create_cards(collection, model_id, deck_id, card):
    # Create card with original text + definition
    note = collection.new_note(model_id)
    note.fields = [
        card['ForeignLanguageWord'],
        card['YourLanguageDefinition'],
        card['YourLanguageImage'],
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


# Updates

# Curried method for changing note type
# Used to build the basic to reverse function below
def change_note_type(old_model_name, new_model_name):
    def wrap(col, note_id):
        if version >= MIN_VERSION:
            old_model = col.models.by_name(old_model_name)
            new_model = col.models.by_name(new_model_name)

            request = ChangeNotetypeRequest()
            request.ParseFromString(col.models.change_notetype_info(old_notetype_id=old_model['id'], new_notetype_id=new_model['id']).input.SerializeToString())
            request.note_ids.extend([ note_id ])
            return col.models.change_notetype_of_notes(request)

    return wrap

# Update the notetype of an existing basic card to a reverse card
# This will add a reverse card to the existing forward card without
# wiping out the stats of the forward card or needing to recreate it
update_basic_to_reverse = change_note_type(nord_basic_fl.model.name, nord_basic_fl_reverse.model.name)
    

# Saving

def save(col): return col.save()


# Initialization

# Initialize a collection handle if necessary
# If col is a string use it to get a collection handle, otherwise return the 
# already open collection handle
def init_handle(col) -> Collection:
    if not col or type(col) is str:
        # Open collection
        col = Collection(col)
    
    return col

from anki.collection import Collection


# Functions for interacting with anki collections

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

# Initialize a collection handle if necessary
# If col is a string use it to get a collection handle, otherwise return the 
# already open collection handle
def init_handle(col) -> Collection:
    if not col or type(col) is str:
        # Open collection
        col = Collection(col)
    
    return col

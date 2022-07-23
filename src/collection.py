# Functions for interacting with anki collections

# Retrieve model id
def get_model_id(col, name):
    return col.models.id_for_name(name)

# Retrieve deck id
def get_deck_id(col, name):
    return col.decks.id_for_name(name)

# Find potential duplicate cards
# Note that deck can be '*' to find duplicates across all decks
def find_dupes(col, deck, fieldname, value):
    cards = col.find_notes(f'\"deck:{deck}\" \"{fieldname}:{value}\"')
    return cards
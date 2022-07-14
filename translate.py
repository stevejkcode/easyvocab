from googletrans import Translator

# Helper function to translate a single word via google translate
# Returns the top translation along with up to 2 alternatives if they are returned by google
# Note this guy can return grammatical gender :(
def translate_word(word, src='fr', dest='en'):
    translator = Translator()
    translation_response = translator.translate(word, dest, src)

    extra_data = translation_response.extra_data
    
    _translation      = extra_data.get('translation')
    _all_translations = extra_data.get('all-translations')

    translations = [_translation[0][0]]

    if _all_translations and _all_translations[0] and len(_all_translations[0][1]) > 0:
        translations.extend(_all_translations[0][1])

    # De-dupe the translations array because sometimes google's api is kinda stoopid
    translations = list(dict.fromkeys(translations))

    translations = translations[:3]

    return [ translation.lower() for translation in translations ]

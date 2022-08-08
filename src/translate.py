import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "site-packages"))

from googletrans import Translator

# Pull global static translator object to prevent continuous re-initializing
translator = Translator()

# Helper to pull and format the foreign language explanation from the response object
# Contains further details such as word type (noun, etc) as well as more detailed
# definitions w/ examples 
def pull_fl_explanation(extra_data, pos):
    definitions = extra_data.get('definitions')

    if definitions is not None and len(definitions) > pos:
        foreign_language_explanation_word_type = definitions[pos][0]
        foreign_language_explanation_details = ""
        
        i = 0
        for definition in definitions[pos][1]:
            text = f'{definition[0]}'

            if len(definition) > 2 and definition[2] is not None: text += f'\n<i>{definition[2]}</i>'

            foreign_language_explanation_details += text

            if i + 1 < len(definitions[pos][1]):
                foreign_language_explanation_details += '<br>'

        return [
            foreign_language_explanation_word_type,
            foreign_language_explanation_details
        ]
    else:
        return [ '', '' ]

# Pull and format the explanation for the user's target language 
# Includes word type (noun, etc) as well as a list of synomyms.
def pull_yl_explanation(extra_data, pos):
    all_translations = extra_data.get('all-translations')

    if all_translations is not None and len(all_translations) > pos:
        your_language_explanation_word_type = all_translations[pos][0]
        your_language_explanation_details = ', '.join([translation for translation in all_translations[pos][1]])

        return [
            your_language_explanation_word_type,
            your_language_explanation_details
        ]
    else:
        return [ '', '' ]


# Translate a single word via google translate
# Returns the top translation along with up to numtrans alternatives if they are returned by google
# Note this guy can't return grammatical gender :(
def translate_word(word, numtrans, src='auto', dest='en'):
    if src is None:
        src = 'auto'

    # Default the number of translations to 1 if it is less than 1
    if numtrans is None or numtrans < 1:
        numtrans = 1

    # translator = Translator()
    translation_response = translator.translate(word, dest, src)

    extra_data = translation_response.extra_data
    
    _translation      = translation_response.text
    _all_translations = extra_data.get('all-translations')

    translations = [_translation]

    if _all_translations and _all_translations[0] and len(_all_translations[0][1]) > 0:
        translations.extend(_all_translations[0][1])

    # De-dupe the translations array because sometimes google's api is kinda stoopid
    translations = list(dict.fromkeys(translations))

    # Truncate the list of translations to the size specified
    translations = translations[ :numtrans ]

    translations = [ translation.lower() for translation in translations ]

    your_language_definition = translations

    [ foreign_language_explanation_word_type_1, foreign_language_explanation_details_1 ] = pull_fl_explanation(extra_data, 0)
    [ foreign_language_explanation_word_type_2, foreign_language_explanation_details_2 ] = pull_fl_explanation(extra_data, 1)
    [ foreign_language_explanation_word_type_3, foreign_language_explanation_details_3 ] = pull_fl_explanation(extra_data, 2)

    [ your_language_explanation_word_type_1, your_language_explanation_details_1 ] = pull_yl_explanation(extra_data, 0)
    [ your_language_explanation_word_type_2, your_language_explanation_details_2 ] = pull_yl_explanation(extra_data, 1)
    [ your_language_explanation_word_type_3, your_language_explanation_details_3 ] = pull_yl_explanation(extra_data, 2)  

    return [
        your_language_definition,
        foreign_language_explanation_word_type_1,
        foreign_language_explanation_details_1,
        foreign_language_explanation_word_type_2,
        foreign_language_explanation_details_2,
        foreign_language_explanation_word_type_3,
        foreign_language_explanation_details_3,
        your_language_explanation_word_type_1,
        your_language_explanation_details_1,
        your_language_explanation_word_type_2,
        your_language_explanation_details_2,
        your_language_explanation_word_type_3,
        your_language_explanation_details_3
    ]

# Auto detect source lang
def detect_lang(word): 
    detect = translator.detect(word)

    lang       = detect.lang
    confidence = detect.confidence

    # If there's more than one lang, take only the first for simplicity
    if lang and type(lang) is list:
        lang = detect.lang[0]
    if confidence and type(confidence) is list:
        confidence = confidence[0]

    return { "lang": lang, "confidence": confidence }

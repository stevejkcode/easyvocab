# Async 
import concurrent.futures

from translate import translate_word

import os
import sys
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "site-packages"))

from googletrans import Translator

words = """a fortiori
s'amonceler
doyenne
épineux
guettent
comblé
redoute
étalé
pansement
bougie
cire
pansement
pèlerinage
péché
aîné 
témoin
achéver""".split('\n')

a = 'blah'

def wrapper(a, f):
    result = f()

    print(a, result)

@wrapper(a)
def f():
    return 5

f()


# def translate(word):
#     translator = Translator()
#     response = translator.translate(word, 'en', 'fr')

#     # response_dict = dict((key, value) for key, value in response.__dict__.iteritems() 
#     #     if not callable(value) and not key.startswith('__'))
#     with open('./response.json', 'w+') as file:
#     #     file.write(json.dumps(json.JSONEncoder().encode(response))
#         _vars = dict(vars(response))
#         del _vars['_response']
#         file.write(json.dumps(_vars))

# translate('gésir')

# notetype = mw.col.models.by_name("prettify-nord-basic_reverse")
# print(notetype)

# print(json.dumps(_vars))
# print(json.dumps(dict(_vars)))

# with concurrent.futures.ProcessPoolExecutor(max_workers = 1) as executor:
#     futures = {}

#     for word in words:
#         futures[executor.submit(translate_word, word, 2, 'fr', 'en')] = word
#     # futures = {executor.submit(translate_word, word, 2, 'fr', 'en'): word for word in words}

#     print(futures)

#     for future in concurrent.futures.as_completed(futures):
#         print('here', future.result(), futures[future])

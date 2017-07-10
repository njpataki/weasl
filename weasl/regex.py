import re
import string
import numpy as np

def _match_regex(rgx, text):
    punct_kw = '(^|\s+|\punct+)' + rgx
    string_punc = ['\%s' % x for x in string.punctuation]
    punct_kw = punct_kw.replace('\punct', '[%s]' % ''.join(string_punc))
    match = re.search(punct_kw, text.lower())
    return match is not None

def regex_search(rgx, text):
    if isinstance(text, str):
        return _match_regex(rgx, text)
    else:
        np.array([_match_regex(rgx, text_item) for text_item in text])
        
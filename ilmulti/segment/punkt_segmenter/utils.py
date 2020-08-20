from .punkt import PunktLanguageVars

# @jerin: Danda and Double Danda lol.
DEVANAGIRI = '\u0964\u0965'
ARABIC_FULL_STOP = '\u06D4'

delimiters = {
    'hi': DEVANAGIRI,
    'bn': DEVANAGIRI,
    'or': DEVANAGIRI,
    'pa': DEVANAGIRI,
    'ur': ARABIC_FULL_STOP
}

def PunktDelimiter(lang):
    # The symbols are obtainable here.
    # https://apps.timwhitlock.info/unicode/inspect?

    lang_delimiters = delimiters.get(lang, '')
    lang_vars_class_name = 'PunktLanguageVars_{}'.format(lang)

    base_end_chars = PunktLanguageVars.sent_end_chars
    sent_end_chars = tuple(list(base_end_chars) + list(lang_delimiters))

    overrides = {
        'sent_end_chars': sent_end_chars
    }

    cls = type(lang_vars_class_name, (PunktLanguageVars,), overrides)
    return cls

def inspect_tokenizer(tokenizer):
    param_keys = ['abbrev_types', 'collocations', 'sent_starters']
    for key in param_keys:
        print(key, getattr(tokenizer._params, key))
        print()

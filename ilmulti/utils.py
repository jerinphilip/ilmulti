
def canonicalize(langcode):
    _variations = {
        "ur": ["ur", "ud"],
        "bn": ["bg", "bn"]
    }

    inverse = {}
    for root in _variations:
        for x in _variations[root]:
            inverse[x] = root

    return inverse.get(langcode, langcode)


def language_token(lang):
    return '__t2{lang}__'.format(lang=lang)

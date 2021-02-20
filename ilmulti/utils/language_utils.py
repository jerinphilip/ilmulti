import warnings

def canonicalize(langcode):
    """
    Fix inconsistent langcodes to a single canonical langcode. Example
    variations like `ud`, `ur` for urdu exists among datasets and this is often
    useful.
    """
    _variations = {
        "ur": ["ur", "ud"],
        "bn": ["bg", "bn"],
        "gu": ["gu", "gj"],
        "pa": ["pa", "pj"]
    }

    inverse = {}
    for root in _variations:
        for x in _variations[root]:
            inverse[x] = root

    return inverse.get(langcode, langcode)


def language_token(lang):
    """ 
    Control token used to indicate a language, often used to indicate which
    target language translate to. Follows a ``__t2<xx>__`` notation.
    """
    return '__t2{lang}__'.format(lang=lang)

def strip_language_token(sample):
    """ 
    Strips language token from a text embedded with a language token using
    language_token().
    """
    language_token, *rest = sample.split()
    return ' '.join(rest)



def inject_token(src_tokenized, tgt_lang):
    """
    Injects a language-token prefix indicating the target language to translate
    to, for a give tokenized string.
    """
    injected_src_tokenized = [
        '{} {}'.format(language_token(tgt_lang), src_tokenized_line)
        for src_tokenized_line in src_tokenized
    ]

    return injected_src_tokenized

def detect_lang(text_sequence, _type="whole"):
    """
    Language detection utility for on-the-fly determination of language. Uses
    langid internally. Two options exist: 

     * `whole` performs this for the entire input.
     * `splitted` breaks and applies language identification to individual sentences
    """
    # Only import langid if required.
    import langid
    langid.set_languages(['ml','ta','bn', 'ur', 'hi', 'en', 'te', 'gu', 'pa', 'mr', 'or'])

    def  _detect_splitted(text_sequence):
        warnings.warn(
            "Detect splitted is not recommended."
            "This might lead to large slowdowns."
        )
        tokens = text_sequence.split()
        lang_assignments = []
        for token in tokens:
            lang, prob = langid.classify(token)
            lang_assignments.append(lang)

        prev = None
        d_idxs = []
        for i, lang in enumerate(lang_assignments):
            if lang != prev:
                d_idxs.append(i)
                prev = lang

        d_idxs.append(len(tokens))

        ranges = zip(d_idxs, d_idxs[1:])
        export = []
        for l, u in ranges:
            sentence = ' '.join(tokens[l:u])
            tpl = (sentence, lang_assignments[l])
            export.append(tpl)

        return export

    def _detect_whole(text_sequence):
        lang, prob = langid.classify(text_sequence)
        return [(text_sequence, lang)]

    switch = {
        "whole": _detect_whole,
        "splitted": _detect_splitted
    }

    if _type not in switch:
        _type = 'whole'
        warnings.warn("Unknown type {}, defaulting to whole".format(_type))

    return switch.get(_type, "whole")(text_sequence)

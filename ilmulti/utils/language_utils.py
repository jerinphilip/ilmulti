import warnings

def canonicalize(langcode):
    """
    This utility function exists to adapt to old naming conventions in
    certain datasets.
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
    return '__t2{lang}__'.format(lang=lang)

def strip_language_token(sample):
    language_token, *rest = sample.split()
    return ' '.join(rest)



def inject_token(src_tokenized,tgt_lang):
    injected_src_tokenized = [
        '{} {}'.format(language_token(tgt_lang), src_tokenized_line)
        for src_tokenized_line in src_tokenized
    ]

    return injected_src_tokenized

def detect_lang(text_sequence, _type="whole"):
    # Only import langid if required.
    import langid
    langid.set_languages(['ml','ta','bn', 'ur', 'hi', 'en', 'te', 'gu', 'pa', 'mr', 'or'])

    def  _detect_segmented(text_sequence):
        warnings.warn(
            "Detect segmented is not recommended."
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
            segment = ' '.join(tokens[l:u])
            tpl = (segment, lang_assignments[l])
            export.append(tpl)

        return export

    def _detect_whole(text_sequence):
        lang, prob = langid.classify(text_sequence)
        return [(text_sequence, lang)]

    switch = {
        "whole": _detect_whole,
        "segmented": _detect_segmented
    }

    if _type not in switch:
        warnings.warn("Unknown type {}, defaulting to whole".format(_type))

    return switch.get(_type, "whole")(text_sequence)

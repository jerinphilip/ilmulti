import langid
import warnings


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


langid.set_languages(['ml','ta','bn', 'ur', 'hi', 'en'])



def detect_lang(text_sequence, _type="whole"):
    def  _detect_segmented(text_sequence):
        # space split first.
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



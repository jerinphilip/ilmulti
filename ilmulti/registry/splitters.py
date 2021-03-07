import os
from . import register_splitter
from ..utils.env_utils import resolve
from ..ssplit import MultiPatternSplitter, MultiPunktSplitter, MultiSimpleSplitter

@register_splitter('simple', MultiSimpleSplitter)
def __simple():
    return {}

@register_splitter('pattern', MultiPatternSplitter)
def __pattern():
    config = {
        "en": {'pattern': "([.;!?…])"},
        "ur": {'pattern': "([.;!?…])"},
        "hi": {'pattern': "([।;!?…|I])" },
        "bn": {'pattern': "([।.;!?…|I])"} ,
        "or": {'pattern': "([।.;!?…|I])"},
    }
    return config

@register_splitter('punkt/pib', MultiPunktSplitter)
def __punkt_pib():
    ASSETS_DIR = resolve()
    data_dir = os.path.join(ASSETS_DIR, 'punkt/pib')   
    path  = lambda lang: os.path.join(data_dir, '{}.pickle'.format(lang))
    langs = [ 'en', 'hi', 'bn', 'ml', 'ur', 'mr', 'gu', 'te', 'ta', 'pa', 'or']
    config = { lang: {'lang': lang, 'path': path(lang)} for lang in langs }
    return config

@register_splitter('punkt/indiccorp', MultiPunktSplitter)
def __punkt_indiccorp():
    ASSETS_DIR = resolve()
    data_dir = os.path.join(ASSETS_DIR, 'punkt/indiccorp')   
    path  = lambda lang: os.path.join(data_dir, '{}.pickle'.format(lang))
    langs = [ "as", "bn", "en", "gu", "hi", "ml", "mr", "or", "pa", "ta", "te"]
    config = { lang: {'lang': lang, 'path': path(lang)} for lang in langs }
    return config

if __name__ == '__main__':
    from . import registry
    print(registry())


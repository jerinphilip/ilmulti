
from .pattern import PatternSplitter, MultiPatternSplitter
from .simple import SimpleSplitter, MultiSimpleSplitter
from .punkt import PunktSplitter, MultiPunktSplitter
from ..utils.env_utils import resolve
import os

def build_splitter(tag='pattern'):
    if tag == 'simple':
        return MultiSimpleSplitter()
    if tag == 'pattern':
        config = {
            "en": {'pattern': "([.;!?…])"},
            "ur": {'pattern': "([.;!?…])"},
            "hi": {'pattern': "([।;!?…|I])" },
            "bn": {'pattern': "([।.;!?…|I])"} ,
            "or": {'pattern': "([।.;!?…|I])"},
        }
        return MultiPatternSplitter.fromConfig(config)
    if tag == 'punkt.pib':
        ASSETS_DIR = resolve()
        data_dir = os.path.join(ASSETS_DIR, 'punkt/pib')   
        path  = lambda lang: os.path.join(data_dir, '{}.pickle'.format(lang))
        langs = [ 'en', 'hi', 'bn', 'ml', 'ur', 'mr', 'gu', 'te', 'ta', 'pa', 'or']
        config = { lang: {'lang': lang, 'path': path(lang)} for lang in langs }
        return MultiPunktSplitter.fromConfig(config)
    raise Exception("Unknown tag")

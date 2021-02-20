
from .pattern import PatternSplitter, MultiPatternSplitter
from .simple import SimpleSplitter
from .punkt import PunktSplitter, MultiPunktSplitter

def build_splitter(tag='pattern'):
    if tag == 'simple':
        return SimpleSplitter()
    if tag == 'pattern':
        return MultiPatternSplitter()
    if tag == 'punkt.pib':
        return MultiPunktSplitter()
    raise Exception("Unknown tag")

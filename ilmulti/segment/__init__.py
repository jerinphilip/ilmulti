
from .pattern_segmenter import Segmenter
from .simple_segmenter import SimpleSegmenter
from .punkt_segmenter import PunktSegmenter

def build_segmenter(tag='pattern'):
    if tag == 'simple':
        return SimpleSegmenter()
    if tag == 'pattern':
        return Segmenter()
    if tag == 'punkt.pib':
        return PunktSegmenter()
    raise Exception("Unknown tag")

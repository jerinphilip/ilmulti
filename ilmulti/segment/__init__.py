
from .segmenters import Segmenter
from .segmenters import SimpleSegmenter

def build_segmenter(tag='pattern'):
    if tag == 'simple':
        return SimpleSegmenter()
    if tag == 'pattern':
        return Segmenter()
    raise Exception("Unknown tag")

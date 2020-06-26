
from .segmenters import Segmenter
from .segmenters import SimpleSegmenter

def build_segmenter(*args, **kwargs):
    return SimpleSegmenter()

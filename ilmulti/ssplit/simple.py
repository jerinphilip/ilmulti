from ..utils import detect_lang
import warnings
from ..meta import ForwardFunctor, PseudoMultiFunctor
from typing import List

class SimpleSplitter(ForwardFunctor):
    def __init__(*args, **kwargs):
        return

    def transform(self, text:str) -> List[str]:
        lines = text.splitlines()
        return lines


class MultiSimpleSplitter(PseudoMultiFunctor):
    Functor = SimpleSplitter

from io import StringIO
from bleualign.align import Aligner
from ilmulti.utils.language_utils import inject_token
from typing import IO, Union, List, Tuple
from ..utils.types import Lang

class BLEUAlign:
    @staticmethod
    def withFiles(src: IO[str], tgt: IO[str], s2t : IO[str] = None, 
            t2s: IO[str] = None) -> Tuple[List[str], List[str]] :

        """
        Internally calls ``bleualign.align``, but allows an API to work directly
        with IO objects. Providing no translations (source to target or target
        to source) leads to Gale Church algorithm.

        :param src: IO object containing source, split in lines.
        :param tgt: IO object containing target, split in lines.
        :param s2t: IO object containing source to target translation, split in lines.
        :param t2s: IO object containing target to source translation, split in lines.

        :return: tuple containing source-lines and target-lines, which are
                 aligned at each index. These needn't correspond to supplied source or
                 target lines (merges of lines can happen).
        """
        output = StringIO()
        options = {
            'srcfile': src,
            'targetfile': tgt,
            'galechurch' : True if s2t is None and t2s is None else False,
            'no_translation_override': True if s2t is None else False,
            'srctotarget': [s2t] if s2t else [],
            'targettosrc': [t2s] if t2s else [],
            'verbosity' : 0,
           }

        a = Aligner(options)
        a.mainloop()
        src_out, tgt_out = a.results()

        srcs = src_out.getvalue().splitlines()
        tgts = tgt_out.getvalue().splitlines()
        return srcs, tgts

    @staticmethod
    def withString(src: str, tgt: str, s2t:str = None, t2s: str = None):
        """
        Characteristics same as :meth:`withFiles`, handles conversion of
        string arguments to IO objects internally to return the processed result.
        """
        src_io = StringIO(src)
        tgt_io = StringIO(tgt)

        maybeStringIO = lambda x: StringIO(x) if x is not None else None
        s2t_io = maybeStringIO(s2t)
        t2s_io = maybeStringIO(tgt_to_src)

        return BLEUAlign.withFiles(src_io, tgt_io, s2t_io, t2s_io);

class BLEUAligner:
    def __init__(self, model=None, tokenizer=None, splitter=None):
        if (model is None and tokenizer is None and splitter is None):
            raise RunTimeError("You seem to have called BLEUAligner without any of model, "
                               "tokenizer or splitter provided. It is suitable to use the functional"
                               "version BLEUAlign in these cases.")
        self.model = model
        self.tokenizer = tokenizer
        self.splitter = splitter

    def _preprocess(self, text: str, lang: str) -> str:
        # If splitter available, split using splitter.
        if splitter is not None:
            text = self.splitter(text, lang=lang)
        else:
            text = text.splitlines()

        # If tokenizer available run one round of tokenizer
        if self.tokenizer is not None:
            text = self.tokenizer.map(texts)

        return '\n'.join(text)

    def _postprocess(self, texts: List[str], lang: Lang) -> List[str]:
        # TODO(jerinphilip): Embeddable SentenceSplitters.
        if self.tokenizer is not None:
            texts = self.tokenizer.inv_map(texts, lang=lang)
        return texts


    def align_blob(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang, 
            s2t: str, t2s: str=None) -> Tuple[List[str], List[str]]:
        src = self._preprocess(src, src_lang)
        tgt = self._preprocess(src, tgt_lang)

        srcs, tgts = BLEUAlign.withString(src, tgt, s2t=s2t);

        srcs = self._postprocess(srcs, src_lang)
        tgts = self._postprocess(tgts, src_lang)

        return srcs, tgts

    # TODO(jerinphilip) It maybe possible to optimize the process by using the
    # model's splitting and tokenizing mechanisms.
    def translate_align_blob(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang):
        src, s2t = self._process_translation_result(self.model(src, tgt_lang=tgt_lang))
        return self.align_blob(src, tgt, src_lang, tgt_lang, s2t);

    def translate_align_bidirectional(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang):
        src, s2t = self._process_translation_result( self.model(src, tgt_lang=tgt_lang))
        tgt, t2s = self._process_translation_result(self.model(tgt, tgt_lang=src_lang))
        return self.align_blob(src, tgt, src_lang, tgt_lang, s2t=s2t, t2s=t2s);

    def _process_translation_result(self, result):
        srcs = [entry['src'] for entry in result]
        s2ts = [entry['tgt'] for entry in result]
        return ('\n'.join(srcs), '\n'.join(s2ts))





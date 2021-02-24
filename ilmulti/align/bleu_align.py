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
        t2s_io = maybeStringIO(t2s)

        return BLEUAlign.withFiles(src_io, tgt_io, s2t_io, t2s_io);

class BLEUAligner:
    def __init__(self, e2e_translator=None, tokenizer=None, splitter=None):
        if (e2e_translator is None and tokenizer is None and splitter is None):
            raise RunTimeError("You seem to have called BLEUAligner without any of e2e_translator, "
                               "tokenizer or splitter provided. It is suitable to use the functional"
                               "version BLEUAlign in these cases.")
        self.e2e_translator = e2e_translator
        self.tokenizer = tokenizer
        self.splitter = splitter

    @classmethod
    def fromE2ETranslator(cls, e2e_translator):
        """
        Convenience method to build from end-to-end translator using the translators tokenizer and splitter.
        """
        return cls(e2e_translator, e2e_translator.tokenizer, e2e_translator.splitter)

    def _preprocess(self, text: str, lang: str, ssplit:bool) -> str:
        # If splitter available, split using splitter.
        if self.splitter is not None and not ssplit:
            text = self.splitter(text, lang=lang)
        else:
            text = text.splitlines()

        # If tokenizer available run one round of tokenizer
        if self.tokenizer is not None:
            text = self.tokenizer.map(text, lang=lang)

        return '\n'.join(text)

    def _postprocess(self, texts: List[str], lang: Lang) -> List[str]:
        # TODO(jerinphilip): Embeddable SentenceSplitters.
        if self.tokenizer is not None:
            texts = self.tokenizer.inv_map(texts)
        return texts

    
    def align(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang, 
            s2t: str, t2s: str=None) -> Tuple[List[str], List[str]]:
        """
        Given a source text, target text and translated text operates with
        tokenizer and splitter instantiated with and provides alignments. Note
        that this function does not use the translation e2e_translator, which is
        expensive.

        :param src: Source text blob
        :param tgt: Target text blob.
        :param s2t: Source to target translation attempt. For best results
                    splitter used on src should provide one to one correspondence to
                    lines in s2t.
        :param t2s: Same as s2t but for target to source, and optional.

        """ 
        return self._align(src, src_lang, tgt, tgt_lang, s2t, t2s, ssplit_src=False, ssplit_tgt=False)

    def _align(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang, 
            s2t: str, t2s: str=None, ssplit_src:bool =False, 
            ssplit_tgt:bool=False) -> Tuple[List[str], List[str]]:

        src = self._preprocess(src, src_lang, ssplit_src) 
        tgt = self._preprocess(tgt, tgt_lang, ssplit_tgt)

        srcs, tgts = BLEUAlign.withString(src, tgt, s2t=s2t, t2s=t2s);

        srcs = self._postprocess(srcs, src_lang)
        tgts = self._postprocess(tgts, src_lang)

        return srcs, tgts

    # TODO(jerinphilip) It maybe possible to optimize the process by using the
    # e2e_translator's splitting and tokenizing mechanisms.
    def align_forward(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang):
        """
        Given a source text, target text and translated text operates with
        tokenizer and splitter instantiated with and provides alignments. Note
        that this function does not use the translation e2e_translator, which is
        expensive.

        :param src: Source text blob
        :param src_lang: 
        :param tgt: Target text blob.
        :param tgt_lang: 

        """ 
        src, s2t = self._process_translation_result(self.e2e_translator(src, tgt_lang=tgt_lang, src_lang=src_lang))
        return self._align(src, src_lang, tgt, tgt_lang, s2t, ssplit_src=True);

    def align_bidirectional(self, src: str, src_lang: Lang, tgt: str, tgt_lang: Lang):
        """
        Same as :meth:`align_forward`, but uses translation in both directions and therefore 2x costly.
        """
        src, s2t = self._process_translation_result( self.e2e_translator(src, tgt_lang=tgt_lang))
        tgt, t2s = self._process_translation_result(self.e2e_translator(tgt, tgt_lang=src_lang))
        return self._align(src, src_lang, tgt, tgt_lang, s2t=s2t, t2s=t2s, ssplit_src=True, ssplit_tgt=True);

    def _process_translation_result(self, result):
        srcs = [entry['src'] for entry in result]
        s2ts = [entry['tgt'] for entry in result]
        return ('\n'.join(srcs), '\n'.join(s2ts))






"""
This file creates models already trained and available.
"""

import os
import sys

import fairseq
import ilmulti

from .args import Args
from .translator import FairseqTranslator
from ..segment import SimpleSegmenter
from ..sentencepiece import SentencePieceTokenizer
from ilmulti.utils import download_resources


class mm_all:
    def __init__(self, root=os.path.join(ilmulti.utils.ILMULTI_DIR, 'mm-all'), use_cuda=False):
        model_path = os.path.join(root, 'model.pt')
        # If not model path, wire to download later.
        if not os.path.exists(model_path):
            url = "http://preon.iiit.ac.in/~jerin/models/mm-all.tar.gz"
            download_resources(url, "mm-all.tar.gz")

        args = Args(
            path=model_path, max_tokens=8000, task='translation',
            source_lang='src', target_lang='tgt', buffer_size=2,
            data=root
        )

        parser = fairseq.options.get_generation_parser(interactive=True)
        default_args = fairseq.options.parse_args_and_arch(parser,
                input_args=['dummy-data'])

        kw = dict(default_args._get_kwargs())
        args.enhance(print_alignment=True)
        args.enhance(**kw)
        fseq_translator = FairseqTranslator(args, use_cuda)
        segmenter = ilmulti.segment.SimpleSegmenter()
        tokenizer = ilmulti.sentencepiece.SentencePieceTokenizer()
        self.engine = ilmulti.translator.MTEngine(fseq_translator, segmenter, tokenizer)

    def __call__(self, *args, **kwargs):
        return self.engine(*args, **kwargs)

    def get_translator(self):
        return self.engine.translator



"""
This file creates models already trained and available.
"""

import os
import requests 
import sys

import fairseq
import ilmulti

from .args import Args
from .translator import FairseqTranslator
from ..segment import SimpleSegmenter
from ..sentencepiece import SentencePieceTokenizer

ILMULTI_DIR = os.path.join(os.environ['HOME'], '.ilmulti')

def download_resources(url, filename, save_path=ILMULTI_DIR):
    fpath = os.path.join(save_path, filename)
    with open(fpath, 'wb') as outfile:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')

        if total is None:
            outfile.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                outfile.write(data)
                done = int(50*downloaded/total)
                sys.stderr.write('\r[{}{}]'.format('█' * done, '.' * (50-done)))
                sys.stderr.flush()
    sys.stdout.write('\n')

class mm_all:
    def __init__(self, root=os.path.join(ILMULTI_DIR, 'mm-all')):
        model_path = os.path.join(root, 'model.pt')
        # If not model path, wire to download later.

        args = Args(
            path=model_path, max_tokens=1000, task='translation',
            source_lang='src', target_lang='tgt', buffer_size=2,
            data=[root]
        )

        parser = fairseq.options.get_generation_parser(interactive=True)
        default_args = fairseq.options.parse_args_and_arch(parser,
                input_args=['dummy-data'])

        kw = dict(default_args._get_kwargs())
        args.enhance(print_alignment=True)
        args.enhance(**kw)
        fseq_translator = FairseqTranslator(args)
        segmenter = ilmulti.segment.SimpleSegmenter()
        tokenizer = ilmulti.sentencepiece.SentencePieceTokenizer()
        self.engine = ilmulti.translator.MTEngine(fseq_translator, segmenter, tokenizer)

    def __call__(self, *args, **kwargs):
        return self.engine(*args, **kwargs)

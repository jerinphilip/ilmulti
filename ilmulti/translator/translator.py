from fairseq.sequence_generator import SequenceGenerator
from collections import namedtuple
import fairseq
# from fairseq import data, options, tasks, tokenizer, utils

import numpy as np
import ilmulti

Batch = namedtuple('Batch', 'srcs tokens lengths')

class TranslatorBase:
    pass

class FairseqTranslator:
    def __init__(self, args, use_cuda=False):
        # In here, we wrap around facebook's translator.
        self.args = args
        self.task = fairseq.tasks.setup_task(args)
        self.use_cuda = use_cuda
        # print('| loading model(s) from {}'.format(args.path))
        model_paths = args.path.split(':')
        models, model_args = fairseq.utils.load_ensemble_for_inference(model_paths, self.task, model_arg_overrides=eval(args.model_overrides))
        self.tgt_dict = self.task.target_dictionary

        # Optimize ensemble for generation
        # print(args.print_alignment)
        for model in models:
            model.make_generation_fast_(
                beamable_mm_beam_size=None if args.no_beamable_mm else args.beam,
                need_attn=args.print_alignment,
            )
            if args.fp16:
                model.half()

        self.max_positions = fairseq.utils.resolve_max_positions(
            self.task.max_positions(),
            *[model.max_positions() for model in models]
        )

        self.translator = SequenceGenerator(
            models, self.tgt_dict, beam_size=args.beam, minlen=args.min_len,
            stop_early=(not args.no_early_stop), normalize_scores=(not args.unnormalized),
            len_penalty=args.lenpen, unk_penalty=args.unkpen,
            sampling=args.sampling, sampling_topk=args.sampling_topk, sampling_temperature=args.sampling_temperature,
            diverse_beam_groups=args.diverse_beam_groups, diverse_beam_strength=args.diverse_beam_strength,
        )
        if self.use_cuda:
            self.translator.cuda()

    def __call__(self, lines, attention=False):
        translations = []
        sources = []
        idxs = []
        for batch, idx in self._make_batches(lines):
            if self.use_cuda:
                src_tokens = batch.tokens.cuda()
                src_lengths = batch.tokens.cuda()

            else:
                src_tokens = batch.tokens
                src_lengths = batch.tokens

            encoder_input = {'src_tokens': src_tokens, 'src_lengths': src_lengths}
            translations_batch = self.translator.generate(
                encoder_input,
                maxlen=int(self.args.max_len_a * batch.tokens.size(1) + self.args.max_len_b),
            )
            sources.extend(batch.tokens)
            translations.extend(translations_batch)
            idxs.extend(idx)

        translations = self._postprocess(lines, sources, translations, attention)
        translations = [x for _, x in sorted(zip(idxs, translations))]
        return translations

    def _postprocess(self, lines, sources, translations, attention):
        align_dict = None
        iterator = zip(lines, sources, translations)
        exports = []
        for idx, itr in enumerate(iterator):
            line, source, _translations = itr
            translation = _translations[0]
            hypo_tokens, hypo_str, alignment = fairseq.utils.post_process_prediction(
                hypo_tokens=translation['tokens'].int().cpu(),
                src_str=source,
                alignment=translation['alignment'].int().cpu() if translation['alignment'] is not None else None,
                align_dict=align_dict,
                tgt_dict=self.tgt_dict,
                remove_bpe=self.args.remove_bpe,
            )
            export = {
                'src' : line,
                'tgt' : hypo_str,
                'attn' : translation['attention'].tolist(),
            }

            if not attention:
                export['attn'] = None


            exports.append(export)
        return exports

    def _make_batches(self, lines):
        task = self.task

        tokens = [
            fairseq.tokenizer.Tokenizer.tokenize(src_str, task.source_dictionary, add_if_not_exist=False).long()
            for src_str in lines
        ]
        lengths = np.array([t.numel() for t in tokens])
        itr = task.get_batch_iterator(
            dataset=fairseq.data.LanguagePairDataset(tokens, lengths, task.source_dictionary),
            max_tokens=self.args.max_tokens,
            max_sentences=self.args.max_sentences,
            max_positions=self.max_positions,
        ).next_epoch_itr(shuffle=False)
        for batch in itr:
            yield Batch(
                srcs=[lines[i] for i in batch['id']],
                tokens=batch['net_input']['src_tokens'],
                lengths=batch['net_input']['src_lengths'],
            ), batch['id']

    def cuda(self):
        self.translator.cuda()
        self.use_cuda = True






if __name__ ==  '__main__':
    from args import multi_args as args
    parser = fairseq.options.get_generation_parser(interactive=True)
    default_args = fairseq.options.parse_args_and_arch(parser)
    kw = dict(default_args._get_kwargs())
    args.enhance(print_alignment=True)
    args.enhance(**kw)
    # print(args)
    tokenizer = ilmulti.sentencepiece.SentencePieceTokenizer()
    translator = FairseqTranslator(args)
    segmenter = ilmulti.segment.Segmenter()
    engine = MTEngine(translator, segmenter, tokenizer)
    translations = engine('hello world', tgt_lang='hi')
    from pprint import pprint
    pprint(translations)

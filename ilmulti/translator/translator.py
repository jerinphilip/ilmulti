from collections import namedtuple
import os

# These are heavy dependencies.
import fairseq
from fairseq.sequence_generator import SequenceGenerator
from fairseq import data, options, tasks, tokenizer, utils

from .args import Args
from ..utils import download_resources, ILMULTI_DIR

Batch = namedtuple('Batch', 'ids src_tokens src_lengths')
Translation = namedtuple('Translation', 'src_str hypos pos_scores alignments')

class FairseqTranslator:
    def __init__(self, args, use_cuda=False):
        # In here, we wrap around facebook's translator.
        self.args = args
        self.task = fairseq.tasks.setup_task(args)
        self.use_cuda = use_cuda
        # print('| loading model(s) from {}'.format(args.path))
        model_paths = args.path.split(':')
        self.models, model_args = fairseq.utils.load_ensemble_for_inference(model_paths, self.task, model_arg_overrides=eval(args.model_overrides))
        self.tgt_dict = self.task.target_dictionary

        # Optimize ensemble for generation
        # print(args.print_alignment)
        for model in self.models:
            model.make_generation_fast_(
                beamable_mm_beam_size=None if args.no_beamable_mm else args.beam,
                need_attn=args.print_alignment,
            )
            if args.fp16:
                model.half()
            if self.use_cuda:
                model.cuda()

        self.max_positions = fairseq.utils.resolve_max_positions(
            self.task.max_positions(),
            *[model.max_positions() for model in self.models]
        )
        self.generator = self.task.build_generator(args)


    def __call__(self, lines, attention=False):
        start_id = 0
        results = []

        args = self.args
        src_dict = self.task.source_dictionary
        tgt_dict = self.task.target_dictionary
        align_dict = utils.load_align_dict(args.replace_unk)

        for batch, idx in self._make_batches(lines):
            src_tokens = batch.src_tokens
            src_lengths = batch.src_lengths
            if self.use_cuda:
                src_tokens = src_tokens.cuda()
                src_lengths = src_lengths.cuda()

            sample = {
                'net_input': {
                    'src_tokens': src_tokens,
                    'src_lengths': src_lengths,
                },
            }
            translations = self.task.inference_step(self.generator, self.models, sample)
            for i, (id, hypos) in enumerate(zip(batch.ids.tolist(), translations)):
                src_tokens_i = utils.strip_pad(src_tokens[i], tgt_dict.pad())
                results.append((start_id + id, src_tokens_i, hypos))


        exports = []
        for id, src_tokens, hypos in sorted(results, key=lambda x: x[0]):
            if src_dict is not None:
                src_str = src_dict.string(src_tokens, args.remove_bpe)
                # print('S-{}\t{}'.format(id, src_str))

            # Process top predictions
            for hypo in hypos[:min(len(hypos), args.nbest)]:
                hypo_tokens, hypo_str, alignment = utils.post_process_prediction(
                    hypo_tokens=hypo['tokens'].int().cpu(),
                    src_str=src_str,
                    alignment=hypo['alignment'].int().cpu() if hypo['alignment'] is not None else None,
                    align_dict=align_dict,
                    tgt_dict=tgt_dict,
                    remove_bpe=args.remove_bpe,
                )
                export = {
                    'src' : src_str,
                    'id'  : id,
                    'tgt' : hypo_str,
                    # 'attn' : translation['attention'].tolist(),
                }

                if not attention:
                    export['attn'] = None

                exports.append(export)
        return exports




    def _make_batches(self, lines):
    # def make_batches(lines, args, task, max_positions, encode_fn):
        args = self.args
        task = self.task
        max_positions = args.max_positions

        encode_fn = lambda x: x
        
        tokens = [
            task.source_dictionary.encode_line(
            encode_fn(src_str), add_if_not_exist=False).long()
            for src_str in lines
        ]

        import torch
        lengths = torch.LongTensor([t.numel() for t in tokens])
        itr = task.get_batch_iterator(
            dataset=task.build_dataset_for_inference(tokens, lengths),
            max_tokens=args.max_tokens,
            max_sentences=args.max_sentences,
            max_positions=max_positions,
        ).next_epoch_itr(shuffle=False)
        for batch in itr:
            yield Batch(
                ids=batch['id'],
                src_tokens=batch['net_input']['src_tokens'], src_lengths=batch['net_input']['src_lengths'],
            ), batch['id']



def build_translator(model, use_cuda=False):
    root = ILMULTI_DIR
    model_path = os.path.join(root, model)
    data = os.path.dirname(model_path)
    if not os.path.exists(model_path):
        raise Exception(
            "The model does not seem downloaded."
            "Please use scripts/download-and-setup.sh before running this code."
        )

    args = Args(
        path=model_path, max_tokens=96000, task='translation',
        source_lang='src', target_lang='tgt', buffer_size=2,
        data=data
    )

    import fairseq
    parser = fairseq.options.get_generation_parser(interactive=True)
    default_args = fairseq.options.parse_args_and_arch(parser, input_args=['dummy-data'])
    keyword_arguments = dict(default_args._get_kwargs())
    args.enhance(print_alignment=True)
    args.enhance(**keyword_arguments)

    fseq_translator = FairseqTranslator(args, use_cuda=use_cuda)
    return fseq_translator



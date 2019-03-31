from collections import deque
from pf.utils import canonicalize

class MultilingualDataset:
    def __init__(self, psets):
        self.psets = psets
        self.langs = set()
        for pset in psets:
            src, tgt = pset.exts
            self.langs.add(src)
            self.langs.add(tgt)

    def __iter__(self):
        self.current = -1
        self.queue = deque()
        self.pset_iter = iter(self.psets)
        self.step()
        return self

    def step(self):
        self.current = self.current + 1
        if self.current >= len(self.psets):
            raise StopIteration
        self.dset = next(self.pset_iter)
        self.iter = iter(self.dset)

    def __next__(self):
        if not self.queue:
            self._refresh()
        return self.queue.popleft()


    def guarded_step(self):
        try:
            content = next(self.iter)
            return content
        except StopIteration:
            self.step()
            content = next(self.iter)
            return content

    def _refresh(self):
        content = self.guarded_step()
        src, tgt = content

        def inject(lang, sequence):
            ltok = '__t2{}__'.format(lang)
            sequence = '{} {}'.format(ltok, sequence)
            return sequence

        lsrc, ltgt = self.current_langs()
        p1 = (inject(ltgt, src), tgt)
        p2 = (inject(lsrc, tgt), src)
        p3 = (inject(lsrc, src), src)
        p4 = (inject(ltgt, tgt), tgt)
        self.queue.append(p1)
        self.queue.append(p2)
        self.queue.append(p3)
        self.queue.append(p4)


    def current_langs(self):
        src, tgt = self.dset.exts
        return src, tgt


class AgnosticTokenizedDataset(MultilingualDataset):
    def __init__(self, psets, tokenizer, monolingual=False):
        super().__init__(psets)
        self.tokenizer = tokenizer
        self.monolingual = monolingual

    def _refresh(self):
        content = self.guarded_step()
        src, tgt = content

        def inject(lang, sequence):
            ltok = '__t2{}__'.format(lang)
            sequence = '{} {}'.format(ltok, sequence)
            return sequence

        lsrc, ltgt = self.current_langs()
        lsrc, ltgt = canonicalize(lsrc), canonicalize(ltgt)

        _lang, src = self.tokenizer(src, lang=lsrc)
        _lang, tgt = self.tokenizer(tgt, lang=ltgt)

        p1 = (inject(ltgt, src), tgt)
        p2 = (inject(lsrc, tgt), src)
        self.queue.append(p1)
        self.queue.append(p2)

        if self.monolingual:
            p3 = (inject(lsrc, src), src)
            p4 = (inject(ltgt, tgt), tgt)
            self.queue.append(p3)
            self.queue.append(p4)

from collections import defaultdict
from itertools import combinations
from . import DATASET_REGISTRY

def select(tags, splits, langs):
    """
    """
    # Filter by split, langs
    registry = dict([
            (k, v)  \
            for k, v in DATASET_REGISTRY.items() \
            if k in tags
    ])

    filtered_corpora = []
    for key in registry:
        _splits, f = registry[key]
        isplits = set(_splits).intersection(set(splits))
        isplits = list(isplits)
        for _split in isplits:
            corpora = f(_split)
            corpora = [
                c for c in corpora \
                if c.lang in langs
            ]

            filtered_corpora.extend(corpora)


    def group_by_tag(corpora):
        _dict = defaultdict(list)
        for corpus in corpora:
            _dict[corpus.tag].append(corpus)
        return _dict

    corpora = group_by_tag(filtered_corpora)
    pairs = []
    for key in corpora:
        for dx, dy in combinations(corpora[key], 2):
            pairs.append((dx, dy))

    return pairs



if __name__ == '__main__':
    tags = ['iitb-hi-en', 'wat-ilmpc']
    splits = ['train']
    langs = ['en', 'hi', 'ta', 'ml']
    pairs = select(tags, splits, langs)
    from pprint import pprint
    pprint(pairs)


from collections import defaultdict
from itertools import combinations

def compile(registry, split, langs):
    """
    """

    # Filter by split, langs
    filtered_corpora = []
    for key in registry:
        _splits, f = registry[key]
        for _split in _splits:
            if _split == split:
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
    from . import DATASET_REGISTRY
    pairs = compile(DATASET_REGISTRY, 'train', ['en', 'hi', 'ml', 'ta'])
    from pprint import pprint
    pprint(pairs)


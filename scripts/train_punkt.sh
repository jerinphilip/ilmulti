#!/bin/bash

set -x;

MONOLINGUAL_PREFIX="../monolingual-exports-pib/raw"
TAG="pib.news"
SAVE_PATH="ilmulti/segment/punkt_segmenter/models"

for LANGCODE in bn en gu hi ml mr or pa ta te ur
do
    ARGS=(
        --train-corpus "$MONOLINGUAL_PREFIX.$LANGCODE"
        --save-model "$SAVE_PATH/$LANGCODE.$TAG.pickle"
        --lang $LANGCODE
    )

    python3 -m ilmulti.segment.punkt_segmenter.train "${ARGS[@]}"
done;

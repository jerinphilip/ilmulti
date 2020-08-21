#!bin/bash

set -x;

SAMPLE_PREFIX='resources/punkt_test_data/pib'
TAG="pib.news"
SAVE_PATH="ilmulti/segment/punkt_segmenter/models"

for LANGCODE in bn en hi ml mr or pa ta te ur
do
    ARGS=(
        --test-corpus "$SAMPLE_PREFIX.$LANGCODE"
        --save-model "$SAVE_PATH/$LANGCODE.$TAG.pickle"
        --lang $LANGCODE
    )

    python3 -m ilmulti.segment.punkt_segmenter.test "${ARGS[@]}"
done;

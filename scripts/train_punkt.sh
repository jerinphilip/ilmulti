#!/bin/bash

set -x;


MONOLINGUAL_PREFIX="../mono-pib/raw"
TAG="pib"
SAVE_PATH="../ilmt-binary-files/punkt/$TAG"
mkdir -p $SAVE_PATH

for LANGCODE in bn en gu hi ml mr or pa ta te ur
do
    ARGS=(
        --train-corpus "$MONOLINGUAL_PREFIX.$LANGCODE"
        --save-model "$SAVE_PATH/$LANGCODE.pickle"
        --lang $LANGCODE
    )

    python3 -m ilmulti.cli.punkt_train "${ARGS[@]}"
done;

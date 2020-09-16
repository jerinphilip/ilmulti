#!/bin/bash

set -x;


# Copy models.

SEVEN_MODELS=(
    # "mm-all"
    # "mm-all+bt"
)

ELEVEN_MODELS=(
    # "mm-all-iter0"
    "mm-all-iter1"
    # "mm-to-en-iter1"
    # "mm-to-en-iter2"
    "mm-to-en-iter3"
)

MODELS=(
    "${SEVEN_MODELS[@]}"
    "${ELEVEN_MODELS[@]}"
)


# HOME='/home/darth.vader'
SAVE_DIR=${HOME}/.ilmulti
BASE_URL="http://preon.iiit.ac.in/~jerin/resources/models"
mkdir -p ${SAVE_DIR}/

echo "Downloading models"

for MODEL in ${MODELS[@]}; do
    MODEL_DIR="${SAVE_DIR}/$MODEL"
    mkdir -p ${MODEL_DIR}
    wget --continue "${BASE_URL}/$MODEL" -O "${MODEL_DIR}/checkpoint_last.pt"
done

for MODEL in ${SEVEN_MODELS}; do 
    MODEL_DIR="${SAVE_DIR}/$MODEL"
    SRC_DIR="$(dirname "$0")/../"
    cp \
        $SRC_DIR/resources/fairseq-dictionaries/ilmulti-v0.dict.txt \
        $MODEL_DIR/dict.src.txt 
    cp \
        $SRC_DIR/resources/fairseq-dictionaries/ilmulti-v0.dict.txt \
        $MODEL_DIR/dict.tgt.txt 
done

for MODEL in ${ELEVEN_MODELS[@]}; do 
    MODEL_DIR="${SAVE_DIR}/$MODEL"
    mkdir -p ${MODEL_DIR}
    SRC_DIR="$(dirname "$0")/../"
    cp \
        $SRC_DIR/resources/fairseq-dictionaries/ilmulti-v1.dict.txt \
        $MODEL_DIR/dict.src.txt 
    cp \
        $SRC_DIR/resources/fairseq-dictionaries/ilmulti-v1.dict.txt \
        $MODEL_DIR/dict.tgt.txt 
done

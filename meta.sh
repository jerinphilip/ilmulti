#!/bin/bash

DATASET=$1
PYTHON=/opt/packages/python/3.6/bin/python3
FAIRSEQ=/Neutron5/jerin/fairseq
DATA=/Neutron5/jerin/parallel-filtering/dumps/$DATASET

set -x

function preprocess {
    cp here/central.dict $DATA/vocab.dict
    $PYTHON $FAIRSEQ/preprocess.py \
        -s src -t tgt              \
        --srcdict $DATA/vocab.dict \
        --tgtdict $DATA/vocab.dict \
        --trainpref $DATA/train    \
        --testpref  $DATA/test     \
        --validpref $DATA/dev      \
        --log-interval 1           \
        --log-format tqdm          \
        --workers 8                \
        --destdir $DATA/data-bin/
}

function preprocess-train {
    cp here/central.dict $DATA/vocab.dict
    $PYTHON $FAIRSEQ/preprocess.py \
        -s src -t tgt              \
        --srcdict $DATA/vocab.dict \
        --tgtdict $DATA/vocab.dict \
        --trainpref  $DATA/train   \
        --log-interval 1           \
        --log-format tqdm          \
        --workers 8                \
        --destdir $DATA/data-bin/
}

function preprocess-test {
    cp here/central.dict $DATA/vocab.dict
    $PYTHON $FAIRSEQ/preprocess.py \
        -s src -t tgt              \
        --srcdict $DATA/vocab.dict \
        --tgtdict $DATA/vocab.dict \
        --testpref  $DATA/test     \
        --log-interval 1           \
        --log-format tqdm          \
        --workers 8                \
        --destdir $DATA/data-bin/
}

function preprocess-dev {
    cp here/central.dict $DATA/vocab.dict
    $PYTHON $FAIRSEQ/preprocess.py \
        -s src -t tgt              \
        --srcdict $DATA/vocab.dict \
        --tgtdict $DATA/vocab.dict \
        --validpref  $DATA/dev     \
        --log-interval 1           \
        --log-format tqdm          \
        --workers 8                \
        --destdir $DATA/data-bin/
}

function copy {
    rsync -rvz --info=progress2 $DATA/data-bin/ ada:/share1/jerin/scale-exps/data/$DATASET/
}

eval "$2"

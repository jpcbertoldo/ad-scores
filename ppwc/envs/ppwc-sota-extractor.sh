#!/usr/bin/env bash
set -e  # stops the execution of a script if a command or pipeline has an

INIT_CONDA_FPATH=${HOME}/init-conda-bash

if [ -f ${INIT_CONDA_FPATH} ]; then
    source ${INIT_CONDA_FPATH}

elif ! command -v conda > /dev/null; then
    echo "[error] conda is not found!"
    exit 1
fi

# src: https://stackoverflow.com/a/56155771/9582881
# i have to do this because otherwise `conda activate` fails
eval "$(conda shell.bash hook)"
echo "[debug] conda=$(which conda)"

echo "installing conda env from yml file"

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR=$(realpath $SCRIPT_DIR)
echo "[debug] SCRIPT_DIR=${SCRIPT_DIR}"

CONDA_ENV_NAME=ppwc-sota-extractor
echo "[debug] CONDA_ENV_NAME=${CONDA_ENV_NAME}"

conda env create --file ${SCRIPT_DIR}/${CONDA_ENV_NAME}.yml
conda activate ${CONDA_ENV_NAME}

# PPWC_SOTA_EXTRACTOR_DIR=$(realpath ${SCRIPT_DIR}/..)
# echo "[debug] PPWC_SOTA_EXTRACTOR_DIR=${PPWC_SOTA_EXTRACTOR_DIR}"

# cd ${PPWC_SOTA_EXTRACTOR_DIR}

# pip install --editable .

echo "[debug] python=$(which python)"

echo "installing the ipykernel locally (--user)"
python -m ipykernel install --user --name=${CONDA_ENV_NAME}

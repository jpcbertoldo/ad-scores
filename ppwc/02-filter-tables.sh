#!/usr/bin/env bash
set -e  # stops the execution of a script if a command or pipeline has an

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR=$(realpath $SCRIPT_DIR)
echo "[debug] SCRIPT_DIR=${SCRIPT_DIR}"

# checking if the python environment is available

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

CONDA_ENV_NAME="ad-scores"
echo "[debug] CONDA_ENV_NAME=${CONDA_ENV_NAME}"

find_in_conda_env(){
    # src
    # https://stackoverflow.com/a/70598193/9582881
    conda env list | grep "${@}" >/dev/null 2>/dev/null
}

if ! find_in_conda_env ${CONDA_ENV_NAME}; then
    echo "[error] conda env ${CONDA_ENV_NAME} not found!"
    echo "please install it first with ad-scores/env/ad-scores.sh"
    exit 1
fi

conda activate ${CONDA_ENV_NAME}
echo "[debug] python=$(which python)"

cd ${SCRIPT_DIR}
echo "[debug] pwd=$(pwd)"

python 02_filter_tables.py

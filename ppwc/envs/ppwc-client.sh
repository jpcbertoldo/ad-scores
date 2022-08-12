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

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR=$(realpath $SCRIPT_DIR)
echo "[debug] SCRIPT_DIR=${SCRIPT_DIR}"

CONDA_ENV_NAME=$(basename ${0%.*})
echo "[debug] CONDA_ENV_NAME=${CONDA_ENV_NAME}"

find_in_conda_env(){
    # src
    # https://stackoverflow.com/a/70598193/9582881
    conda env list | grep "${@}" >/dev/null 2>/dev/null
}

ENV_YML_FPATH="${SCRIPT_DIR}/${CONDA_ENV_NAME}.yml"
echo "[debug] ENV_YML_FPATH=${ENV_YML_FPATH}"

if ! find_in_conda_env ${CONDA_ENV_NAME}; then
    echo "conda env CONDA_ENV_NAME=${CONDA_ENV_NAME} not found!"
    echo "installing conda env from yml file"
    conda env create --file ${ENV_YML_FPATH}
else 
    echo "conda env CONDA_ENV_NAME=${CONDA_ENV_NAME} found!"
    echo "updating conda env from yml file"
    conda env update --name ${CONDA_ENV_NAME} --file ${ENV_YML_FPATH} --prune
fi

echo "activating conda env CONDA_ENV_NAME=${CONDA_ENV_NAME}"

conda activate ${CONDA_ENV_NAME}
echo "[debug] python=$(which python)"

echo "installing the ipykernel locally (--user) with --name=${CONDA_ENV_NAME}"
python -m ipykernel install --user --name=${CONDA_ENV_NAME}


#!/usr/bin/env bash
set -e  # stops the execution of a script if a command or pipeline has an

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR=$(realpath $SCRIPT_DIR)
echo "[debug] SCRIPT_DIR=${SCRIPT_DIR}"

DATA_LINKS_FPATH="${SCRIPT_DIR}/00-data-links.txt"
echo "[debug] DATA_LINKS_FPATH=${DATA_LINKS_FPATH}"

DATA_DIR=${SCRIPT_DIR}/data
echo "[debug] DATA_DIR=${DATA_DIR}"

LINKS=( $( cat ${DATA_LINKS_FPATH} ) )

for LINK in ${LINKS[@]}; do
    echo "[debug] LINK=${LINK}"
    GZ_FILE_NAME=$( basename ${LINK} )
    echo "[debug] GZ_FILE_NAME=${GZ_FILE_NAME}"
    wget -O ${DATA_DIR}/${GZ_FILE_NAME} ${LINK} 
    gunzip --force ${DATA_DIR}/${GZ_FILE_NAME}
done
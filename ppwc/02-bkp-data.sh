#!/usr/bin/env bash
set -e  # stops the execution of a script if a command or pipeline has an

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR=$(realpath $SCRIPT_DIR)
echo "[debug] SCRIPT_DIR=${SCRIPT_DIR}"

DATA_LINKS_FPATH="${SCRIPT_DIR}/00-data-links.txt"
echo "[debug] DATA_LINKS_FPATH=${DATA_LINKS_FPATH}"

DATA_DIR=${SCRIPT_DIR}/data
echo "[debug] DATA_DIR=${DATA_DIR}"

TODAY=$(date +'%Y-%m-%d')
echo "[debug] TODAY=${TODAY}"

BKP_DIR=${SCRIPT_DIR}/bkp
echo "[debug] BKP_DIR=${BKP_DIR}"

BKP_ZIP_FNAME=${TODAY}-all-data.zip
echo "[debug] BKP_ZIP_FNAME=${BKP_ZIP_FNAME}"

EXCLUDED_FILES="${DATA_DIR}/papers-with-abstracts.json"
echo "[debug] EXCLUDED_FILES=${EXCLUDED_FILES}"

mkdir -p ${BKP_DIR}
zip -r ${BKP_DIR}/${BKP_ZIP_FNAME} ${DATA_DIR} -x ${EXCLUDED_FILES}

ls -lh ${BKP_DIR} | grep ${BKP_ZIP_FNAME}

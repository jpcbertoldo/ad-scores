#!/usr/bin/env bash
set -e  # stops the execution of a script if a command or pipeline has an

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
SCRIPT_DIR=$(realpath $SCRIPT_DIR)
echo "[debug] SCRIPT_DIR=${SCRIPT_DIR}"

README_FPATH="${SCRIPT_DIR}/paperswithcode-data/README.md"
echo "[debug] README_FPATH=${README_FPATH}"

cat ${README_FPATH} | grep -o 'https://.*\.json\.gz' | sort -u > ${SCRIPT_DIR}/00-data-links.txt

cat ${SCRIPT_DIR}/00-data-links.txt
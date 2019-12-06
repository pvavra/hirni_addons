#!/usr/bin/env bash
# simple wrapper around helpers/unpack-studyspec.py which will call datalad run

set -e -u
set -x

folder=$(dirname "$0")
if [ "$#" -gt 1 ]
then
    datalad run --explicit --input "$1" --output "$2" python $folder/../helpers/unpack_studyspec.py "$1" "$2"
else
    datalad run --explicit --input "$1" --output "$1" python $folder/../helpers/unpack_studyspec.py "$1" "$1"
fi

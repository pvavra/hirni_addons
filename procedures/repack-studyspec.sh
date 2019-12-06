#!/usr/bin/env bash
# simple wrapper around helpers/repack-studyspec.py which will call datalad run

set -e -u
set -x

d_me=$(dirname "$0")
helpers="$d_me/../helpers"
in_file="$1"

if [ "$#" -gt 1 ]
then
    out_file="$2"
else
    out_file="$1"
fi

datalad run --explicit --input "$in_file" --output "$out_file" python "$helpers"/repack_studyspec.py "$in_file" "$out_file"

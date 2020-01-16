#!/usr/bin/env bash
#
# simple wrapper around matlab and `converter/behavior-converter.m`


set -e -u
set -x

d_me=$(dirname "$0")
converter="$d_me/../converter/behavior-converter.m"
# ds="$1"


call-format = "matlab -nojvm -nodisplay -nosplash -r $converter $ds $@"

datalad run --explicit --input "$in_file" --output "$out_file" python "$helpers"/repack_studyspec.py "$in_file" "$out_file"

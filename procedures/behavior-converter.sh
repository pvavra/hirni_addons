#!/usr/bin/env bash
#
# simple wrapper around matlab and `converter/behavior-converter.m`


set -e -u
set -x

d_me=$(dirname "$0")
ds="'$1'"
file_input="'$2'"
subject="'$3'"
session="'$4'"

dir_converter="$d_me/../converter"

call="converter_behavior($file_input, $subject, $ds, $session)"

# ds="$1"

pushd "$dir_converter"
matlab -nodisplay -nosplash -singleCompThread -r "$call; exit"
popd

# fi
# TODO: use datalad run with input/output defs to avoid saving more than
#  created by the current procedure
datalad save -m "added events.tsv files for sub-$subject/ses-$session"

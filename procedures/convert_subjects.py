"""
Procedure to convert imported dicoms to bids
Should be called from with sourcedata (to enable custom-rules)

The procedure should be called with the following arguments:
    datalad run-procedure convert_subjects subjects.json /path/to/bids_dir

The subjects.json file should be a valid json array of objects, like:

[
    {"anon-sub": "007", "acq": "jb68_0007"},
    {"anon-sub": "007", "acq": "jb68_0008"}
]

This script automatically fills out that part for us, using the
following template:

datalad hirni-spec2bids -d .. --anonymize sourcedata/{acq}/studyspec.json

"""

import sys
from datalad.distribution.dataset import require_dataset
import os
import json

# define expected keys:
key_acq = "acq"

ds = require_dataset(
    sys.argv[1],
    check_installed=True,
    purpose='convert specs to bids')

file_subject = sys.argv[2]
target_dir = sys.argv[3]

ds_bids = require_dataset(
    target_dir,
    check_installed=True,
    purpose='adding niftis')

if not os.path.isfile(file_subject):
    sys.exit("json-file not found")

f = open(file_subject, "r")
list = json.load(f)

for item in list:
    if key_acq in item:

        cmd = ("datalad hirni-spec2bids -d {target} --anonymize"
            " sourcedata/{acq}/studyspec.json".format(
            acq=item[key_acq],
            target=target_dir
            ))
        print("[Hirni ADDONS] Running following command:")
        print("[Hirni ADDONS] {}".format(cmd))
        os.system(cmd)

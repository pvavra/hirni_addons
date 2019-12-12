"""
Procedure to import subjects based on a subjects.json

The procedure should be called with the following arguments:
    datalad run-procedure import_subjects subjects.json /path/to/source

The subjects.json file should be a valid json array of objects, like:

[
    {"anon-sub": "007", "acq": "jb68_0007"},
    {"anon-sub": "007", "acq": "jb68_0008"}
]

In our specific use-case, inside the source directory is there is a subfolder
called `jb68_0007` inside which the relevant .tar-file also starts with that
string.  This script automatically fills out that part for us, using the
following template:

datalad --pbs-runner condor hirni-import-dcm \
    --anon-subject {anon-sub} {source}/{acq}/{acq}*.tar {acq}

"""

import sys
from datalad.distribution.dataset import require_dataset
import os
import json

# define expected keys:
key_anon = "anon-sub"
key_acq = "acq"

ds = require_dataset(
    sys.argv[1],
    check_installed=True,
    purpose='adding custom rule')

file_subject = sys.argv[2]
source_dir = sys.argv[3]

if not os.path.isdir(source_dir):
    sys.exit("source directory not valid")
if not os.path.isfile(file_subject):
    sys.exit("json-file not found")

f = open(file_subject, "r")
list = json.load(f)

for item in list:
    if key_anon in item and key_acq in item:

        # check whether the target dicoms have already been imported, if yes,
        # skip now
        if os.path.isdir("{ds_path}/{acq}".format(
            ds_path=ds.path,
            acq=item[key_acq])):

            print("[Hirni ADDONS] Acquisition {} "
                "already present - skipping".format(item[key_acq]))
            continue

        cmd = ("datalad --pbs-runner condor hirni-import-dcm "
            "--anon-subject {anon} {s}/{acq}/{acq}*.tar {acq}".format(
            anon=item[key_anon],
            s=source_dir,
            acq=item[key_acq]
            ))
        print("[Hirni ADDONS] Running following command:")
        print("[Hirni ADDONS] {}".format(cmd))
        os.system(cmd)

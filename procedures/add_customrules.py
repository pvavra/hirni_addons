"""Procedure to configure custom rules for dicom2spec"""

import sys
import os.path as op

from datalad.distribution.dataset import require_dataset

ds = require_dataset(
    sys.argv[1],
    check_installed=True,
    purpose='adding custom rule')

# grab config
cfg = ds.config

# TODO: what to do when a rules is already present? abort? overwrite?
cfg.add('datalad.hirni.dicom2spec.rules',
        # we assume that hirni_addons have been installed into `sourcedata/code/.`
        op.join("code","hirni_addons", "custom_rules", "custom_rules.py"),
        where='dataset')

ds.save(message="add custom_rules.py to dataset configuration")

#!/bin/bash
# To be run from within sourcedata/
i=001; datalad hirni-dicom2spec -s "sub-$i/studyspecs.json"  -d . --subject "$i" --anon-subject "$i"  --acquisition "sub-$i" "sub-$i/dicoms"

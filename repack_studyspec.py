#!/usr/bin/env python
import sys
import json as js
import datalad.support.json_py as jslad


in_file = sys.argv[1]
if len(sys.argv) > 2:
    out_file = sys.argv[2]
else:
    out_file = in_file

with open(in_file, mode='r') as f:
    specs = js.load(f)

# write out to file
jslad.dump2stream(specs, out_file)

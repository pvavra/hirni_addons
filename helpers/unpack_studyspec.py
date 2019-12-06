#!/usr/bin/env python
import sys
import json as js
import datalad.support.json_py as jslad

in_file = sys.argv[1]
if len(sys.argv) > 2:
    out_file = sys.argv[2]
else:
    out_file = in_file

spec_list = jslad.load_stream(in_file)

# convert to valid json string
enc = js.JSONEncoder(sort_keys=False, indent=4)
content = "["
for spec_dict in spec_list:
     content += enc.encode(spec_dict)
     content += ",\n"
content = content[:-2] # remove trailing ",\n"
content += "]\n"

with open(out_file, "w") as f:
    f.write(content)

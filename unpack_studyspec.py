#!/usr/bin/env python
import sys
import json as js
import codecs

in_file = sys.argv[1]
if len(sys.argv) > 2:
    out_file_json = sys.argv[2]
else:
    out_file_json = in_file


dec = js.JSONDecoder()
enc = js.JSONEncoder(sort_keys=False, indent=4)
content = "["
with open(in_file, mode='rb') as f:
    jreader = codecs.getreader('utf-8')(f)
    for line in jreader:
        unpacked = dec.decode(line)
        content += enc.encode(unpacked)
        content += ',\n'
# remove last comma
content = content[:-2]
content += "]\n"

with open(out_file_json, "w") as write_file:
    write_file.write(content)

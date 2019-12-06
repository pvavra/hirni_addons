#!/usr/bin/env python
import sys
import json as js
import codecs

in_file = sys.argv[1]
if len(sys.argv) > 2:
    out_file_json = sys.argv[2]
else:
    out_file_json = in_file

with open(in_file, mode='rb') as f:
    specs = js.load(f)

enc = js.JSONEncoder(separators=(',', ':'))

with open(out_file_json, "wb") as f:
    jwriter = codecs.getwriter('utf-8')(f)
    for spec in specs:
        line = enc.encode(spec)
        jwriter.writelines(line)
        f.write(b'\n')

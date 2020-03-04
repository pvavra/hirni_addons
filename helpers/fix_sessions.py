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

new_spec_list = []
session_dict = {"value" : []}

for spec_dict in spec_list:
     if spec_dict["type"] == 'events_file':
         filename = spec_dict["location"]
         session = filename.split("day")[1][0]

         spec_dict["bids-session"] = {"value" : session.zfill(3)}
         print("for file ''" + filename +"' set session to "+session.zfill(3))
     new_spec_list.append(spec_dict)


# print(new_spec_list)
jslad.dump2stream(new_spec_list, out_file)

#!/usr/bin/env python

import json
import os
from subprocess import call

module_names = []


with open("external-scripts-input.json") as data_file:
    scripts = json.load(data_file)
    for script in scripts:
        call(["yarn", "add", script])
        module_name = script
        if "/" in script:
            module_name = os.path.splitext(os.path.basename(script))[0]
        if "#" in module_name:
            module_name = module_name.split("#")[0]
        module_names.append('"' + module_name + '"')

with open("external-scripts.json", "w") as install_file:
     install_file.write("[" + ",".join(module_names) + "]")

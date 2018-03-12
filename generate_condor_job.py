#!/usr/bin/env python
from __future__ import absolute_import, division, print_function, unicode_literals
import os, stat

project_name = raw_input("Name of project (no spaces - i.e. cube): ")
filename = raw_input("Name of .feb file: ")
if ".feb" not in filename:
    filename += ".feb"
script_name = project_name + ".sh"
job_name = project_name + ".sub"
log_name = project_name + ".log"
output_name = project_name + ".output"


with open(script_name, "w") as script_file:
    script_file.write("#!/bin/bash\n/home/medialab/febio-2.6.4/bin/febio2.lnx64 -i " + filename + '\n')

with open(job_name, "w") as job_file:
    job_file.write("""executable = {0}
        log = {1}
        output = {2}
        arguments = \"{3}\"
        transfer_input_files = {4}
        error = error.txt
        should_transfer_files = Yes
        queue\n""".format(script_name, log_name, output_name, filename, filename))


st = os.stat(script_name)
os.chmod(script_name, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
print("Successfully created condor job files. Script is located at {}, submission is located at {}".format(script_name, job_name))

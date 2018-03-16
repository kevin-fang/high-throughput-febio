#!/usr/bin/env python
import os, stat

# get project name and file name of feb file
project_name = raw_input("Name of project (no spaces - i.e. cube): ")
filename = raw_input("Name of .feb file: ")
if ".feb" not in filename: # append the .feb extension if necessary
    filename += ".feb"
machine_req = raw_input("Set machine requirements? [Y/n] ").lower()
ram_req = 0
cpu_req = 0
if machine_req == "yes" or machine_req == "y":
    ram_req = input("RAM requirement (MB): ")
    cpu_req = input("CPU requirement (# cores): ")


# generate names for condor job creation
script_name = project_name + ".sh"
job_name = project_name + ".sub"
log_name = project_name + ".log"
output_name = project_name + ".output"

FEBIO_LOCATION = '/home/medialab/febio-2.6.4/bin/febio2.lnx64'

# write the FEBio script to a file
with open(script_name, "w") as script_file:
    script_file.write("#!/bin/bash\n" + FEBIO_LOCATION + " -i $1\n")
# make the script executable
st = os.stat(script_name)
os.chmod(script_name, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

# generate the condor job
with open(job_name, "w") as job_file:
    job_file.write("""executable = {0}
log = {1}
output = {2}
arguments = \"{3}\"
transfer_input_files = {4}
request_memory = {5}
request_cpus = {6}
error = error.txt
should_transfer_files = Yes
queue\n""".format(script_name, log_name, output_name, filename, filename, ram_req, cpu_req))

print("Successfully created condor job files. Script is located at {}, submission is located at {}".format(script_name, job_name))

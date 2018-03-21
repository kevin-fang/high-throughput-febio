#!/usr/bin/env python3
import os, stat, errno, sys

import argparse
parser = argparse.ArgumentParser(description='Create a job submission file for HTCondor')
parser.add_argument("--project_name", default="job", help="Set a file name for the job submission file (default: \"job\")")
parser.add_argument("--folder", required=True, help="Folder containing .feb files")
parser.add_argument("--cpu_req", type=int, default=0, help="Number of CPU cores required for each job (default: 0)")
parser.add_argument("--ram_req", type=int, default=0, help="MB of RAM required for each job (default: 0)")
args = parser.parse_args()

folder_name = args.folder
project_name = args.project_name
cpu_req = args.cpu_req
ram_req = args.ram_req

# location where FEBio is located
FEBIO_LOCATION = '/home/medialab/febio-2.6.4/bin/febio2.lnx64'
script_name = "febio.sh"

# make sure that an output directory is generated, because HTCondor does not automatically do it
try:
    os.makedirs('./output')
    print("Creating output folder...")
except OSError as e:
    if e.errno == errno.EEXIST:
        print("Output folder already exists. Continuing...")
    else:
        raise

# write the FEBio script
with open(script_name, "w") as script_file:
    script_file.write("#!/bin/bash\n" + FEBIO_LOCATION + " -i $1\n")
    
# make the script executable
st = os.stat(script_name)
os.chmod(script_name, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)

# generate a job from a filenmae
def generate_job(filename, input_dir):
    # remove the .feb extension
    truncated_filename = filename[0:-4]
    return """arguments = {filename}
transfer_input_files = {input_dir}/{filename}
output = output/{truncated_filename}.out
error = output/{truncated_filename}.err
transfer_output_files = {truncated_filename}.xplt, {truncated_filename}.log
log = output/{truncated_filename}.log
transfer_output_remaps = \"{truncated_filename}.xplt=./output/{truncated_filename}.xplt; {truncated_filename}.log=./output/{truncated_filename}.log\"
queue

""".format(filename = filename, truncated_filename = truncated_filename, input_dir = input_dir)

job_name = project_name + ".sub"

# generate the condor job
with open(job_name, "w") as job_file:
    job_file.write(
""" #initialize
executable = febio.sh
universe = Vanilla
should_transfer_files = Yes
request_memory = {}
request_cpus = {}

""".format(ram_req, cpu_req))
    # iterate through the feb directory, adding a job for each one
    for filename in os.listdir(folder_name):
        if filename.endswith(".feb"):
            job_file.write(generate_job(filename, folder_name))
        else:
            print("Skipping " + filename + " (doesn't end in .feb) ")

print("\nSuccessfully generated job. Run condor_submit {} to start the job.".format(job_name))

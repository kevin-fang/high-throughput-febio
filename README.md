# Finite Element Analysis with High Throughput Computing   

Kevin Fang, Biomechatronics @ MIT Media Lab, March 2018

Set up a cluster of computers for high throughput computing to run computational analysis. This specific repository applies to using FEBio, software for finite element analysis. However, this idea can be applied to any project that has lots of files that need to be processed.

This repository uses [HTCondor](https://research.cs.wisc.edu/htcondor/), high throughput compute software created by UW-Madison. The goal of this project is to create a network that distributes many complex software jobs (e.g. thousands of optimization problems) to lots of computers. Running a single very intense workload (e.g. a single 15 hour calculation) would be better suited for other networks.

---

## About

The `generate_condor_job.py` script creates two files: a script for FEBio, and a job submission file for Condor. The script simply looks like this (the FEBio location may need to be changed - change it by modifying the `FEBIO_LOCATION` variable in the Python script):  
```
#!/bin/bash
/home/medialab/febio-2.6.4/bin/febio2.lnx64 -i <filename>
```

The job submission file looks like this:  
```
executable = <script name>
log = <log name>
output = <output name>
arguments = <.feb filename>
transfer_input_files = <.feb filanem>
error = error.txt
should_transfer_files = Yes
queue
```

Once these two files are created, move them to the same directory as the .feb file. Check that the Condor cluster is active with `condor_status`, and if it is, simply run `condor_submit <submission file>.sub` and wait for the cluster to run the analysis (the output of condor_submit should be `<num_jobs> job(s) submitted to cluster <cluster_num>`. You can check on the status of the jobs with `condor_q`, or for a more detailed status, write `condor_q -analyze <cluster_num>`.

---

### Notes  
[INSTALL.md](INSTALL.md) contains installation instructions. Take a look at `sample_condor_config.local` for a sample condor config. The docker install uses this when building an image.

### To do:  
- Make a condor config builder? Make a Dockerfile builder (AKA Docker image builder builder)?  
- Make a user friendly method of submitting jobs - perhaps a web server with Node.js/React.js?
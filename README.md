# Finite Element Analysis with High Throughput Computing   

Kevin Fang, Biomechatronics @ MIT Media Lab, March 2018

Set up a cluster of computers for high throughput computing to run computational analysis. This specific repository applies to using FEBio, software for finite element analysis. However, this idea can be applied to any project that has lots of files that need to be processed.

---

## About

This repository uses [HTCondor](https://research.cs.wisc.edu/htcondor/), high throughput compute software created by UW-Madison. The goal of this project is to create a network that distributes many complex software jobs (e.g. thousands of optimization problems) to lots of computers. Running a single very intense workload (e.g. a single 15 hour calculation) would be better suited for other networks. 

---

### Installation  
[INSTALL.md](INSTALL.md) contains important installation instructions on how to set up the Condor network

--- 

### Python scripts

`generate_from_directory.py` takes a job name and directory as input. It generates a single submission file that creates a job to run FEBio on every single file in the provided directory.

`generate_condor_job.py` creates a job for a single submission. 

Both of these scripts create a `.sub` file for to be submitted, and a file called `febio.sh` that contains the command for each execution machine to run. 

Once these files are created, check that the Condor cluster is active with `condor_status`, and if it is, simply run `condor_submit <submission file>.sub` and wait for the cluster to run the analysis (the output of condor_submit should be `<num_jobs> job(s) submitted to cluster <cluster_num>`. You can check on the status of the jobs with `condor_q`, or for more detailed analysis, write `condor_q -analyze <cluster_num>`.

### To do:  
- Make a user friendly method of submitting jobs - perhaps a web server with Node.js/React.js?
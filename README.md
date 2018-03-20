# Finite Element Analysis with High Throughput Computing  
Kevin Fang, Biomechatronics @ MIT Media Lab, March 2018

Distribute finite element analysis jobs to a cluster of computers running Linux using HTCondor. This specific repository applies to using FEBio. However, this idea can be applied to any project that has lots of files that need to be processed.

---

## About

This repository uses [HTCondor](https://research.cs.wisc.edu/htcondor/), high throughput compute software created by UW-Madison. The goal of this project is to create a network that distributes many complex software jobs (e.g. thousands of optimization problems) to lots of computers. This network does not do well with running a single, very intense workload (e.g. one 15 hour calculation).  

---

### Installation  
[INSTALL.md](INSTALL.md) contains important installation instructions on how to set up the Condor network. 

--- 

### Python scripts

`generate_from_directory.py` takes a job name and directory as input. It generates a single submission file that creates a job to run FEBio on every single file in the provided directory.

`generate_condor_job.py` creates a job for a single submission. 

Both of these scripts create a `.sub` file for to be submitted, and a file called `febio.sh` that contains the command for each execution machine to run.  

---

## Using HTCondor for FEBio

Once you follow the [installation instructions](INSTALL.md), you can submit jobs through the central manager. Technically, any machine can submit jobs for the central manager to process.

Create a new directory for your project (let's call it `project_directory/`). In `project_directory/`, create a folder to hold the FEBio files (call it `files/`) and copy all the `.feb` files to that directory. Copy the Python script `generate_from_directory.py` in this repository to `project_directory/`. Run `python3 generate_from_directory.py` and follow the instructions to generate a job submission (we'll call this project "sample_job").

Once the Python script is run, the `project_directory/` should look like this:  
```
project_directory/
├───generate_from_directory.py
├───febio.sh
├───sample_job.sub
├───output
│   └───[empty]
└───files
    ├───model1.feb
    ├───model2.feb
    └───model3.feb
```

- On the central manager, check that the Condor cluster is active with `condor_status`. If it prints a list of machines, that means that your setup was successful.  
- Run `condor_submit <submission file>.sub` and wait for the cluster to run the analysis (the output of `condor_submit` should be `<num_jobs> job(s) submitted to cluster <cluster_num>`).  
- Check on the status of the jobs with `condor_q`, or for more detailed analysis, write `condor_q -analyze <cluster_num>`. The output of the jobs can be found in a new directory called `output/`.
- After the analysis is finished, `project_directory/` would look like this:  
```
project_directory/
├───generate_from_directory.py
├───febio.sh
├───sample_job.sub
├───output
│   ├───model1.err
│   ├───model1.log
│   ├───model1.out
│   ├───model1.xplt
│   ├───model2.err
│   ├───model2.log
│   ├───model2.out
│   ├───model2.xplt
│   ├───model3.err
│   ├───model3.log
│   ├───model3.out
│   └───model3.xplt
└───files
    ├───model1.feb
    ├───model2.feb
    └───model3.feb
```

## Expanding beyond FEBio  
This repo can easily be modified to work with other command line processing software besides FEBio, but it involves knowing Docker, Python, and Condor, and requires a basic understanding of `generate_from_directory.py`. To use it with other software:  
- Change the Dockerfile such that it installs the needed software in the image (e.g. if you're running MatLab, modify the Dockerfile so that it installs MatLab).  
- Modify `generate_from_directory.py` so that `script_file` contains a command line argument to run the command line software. To feed in parameters, use `$1`.  
- Modify the `generate_job` function in `generate_from_directory.py` so that it has the correct input/output names and redirects output correcty.

### To do:  
- Make a user friendly method of submitting jobs - perhaps a web server with Node.js/React.js?
- Create documentation for submitting jobs from other machines if the central manager is not easily accessible.
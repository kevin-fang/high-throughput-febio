# Finite Element Analysis with High Throughput Computing  
Kevin Fang, Biomechatronics @ MIT Media Lab, March 2018

Distribute finite element analysis jobs to a cluster of computers running Linux using HTCondor. This specific repository applies to using FEBio. However, this idea can be applied to any project that has lots of files that need to be processed.

---

## About

This repository uses [HTCondor](https://research.cs.wisc.edu/htcondor/), high throughput compute software created by UW-Madison. The goal of this project is to create a network that distributes many complex software jobs (e.g. thousands of optimization problems) to lots of computers. This network does not do well with running a single, very intense workload (e.g. one 15 hour calculation).  

---

### Installation  
[INSTALL.md](INSTALL.md) contains important installation instructions on how to set up the Condor network.  
Complete list of steps to follow from INSTALL.md:  
1. Set up a central manager (either using the [Docker](INSTALL.md#user-content-initializing-through-docker)) or [native](INSTALL.md#user-content-native-installation) method). In `condor_config.local`, set `DAEMON_LIST` to `MASTER, COLLECTOR, NEGOTIATOR, SCHEDD` and optionally addd `STARTD` if you want your central manager to be able to execute jobs to. Record the IP address of this computer.
2. Set up execution machines (either Docker/native). Set [slot definitions](INSTALL.md#user-content-setting-condor_configlocal). In `condor_config.local`, set CONDOR_HOST equal to the IP address of the central manager. If you are deploying to a large configuration, it would be easiest to distribute the same configuration file to all the machines.
3. Once the native/Docker installations are all up, run `condor_status` on the central manager and make sure that you see all the machines.  
4. Follow the Python script instructions below for creating jojbs.


--- 

### Using the Python scripts with Condor

`generate_from_directory.py` generates a single submission file that creates a job to run analysis on several .feb files in a directory. It takes the following arguments:  
- `--folder` (required) points to the directory containing the .feb files (e.g. `--folder ./files`).
- `--project_name` (optional) sets a project name for the output job file. Default is `job.sub`.
- `--ram_req` (optional) sets a RAM requirement in megabytes for computers able to execute the job.
- `--cpu_req` (optional) sets a CPU requirement in number of cores for computers able to execute the job.
- `--run` - if this is included, immediately after generating the job submission file the program will submit the job to the cluster.

The generated files will be located in a directory called `output/`.

The script creates a `.sub` file to be submitted, and a file called `febio.sh` that contains the command for the execution machines to run.  

For example, if you have .feb files located in a directory called `feb_directory/`, run `python3 generate_from_directory.py --folder feb_directory --job sample_job` and follow the instructions to generate a job submission. Once the script is run, `feb_directory/` should look like this:  
```
feb_directory/
├───model1.feb
├───model2.feb
├───model3.feb
└───output/
   ├───sample_job.sub
   └───febio.sh

```

- If you want to submit the job immediately, you would run `python3 generate_from_directory.py --folder feb_directory --job sample_job --run` instead.  
- If you did not include `--run`, navigate to `output/` and run `condor_submit <submission file>.sub` and wait for the cluster to run the analysis (the output of `condor_submit` should be `<num_jobs> job(s) submitted to cluster <cluster_num>`).  
- Check on the status of the jobs with `condor_q`, or for more detailed analysis, write `condor_q -analyze <cluster_num>`. The output of the jobs can be found in a new directory called `output/`.
- After the analysis is finished, `project_directory/` would look like this:  
```
feb_directory/
├───model1.feb
├───model2.feb
├───model3.feb
└───output/
   ├───sample_job.sub
   ├───model1.txt, model1.log, model1.err + model1 outputs
   ├───model2.txt, model2.log, model2.err + model2 outputs
   ├───model3.txt, model3.log, model3.err + model3 outputs
   └───febio.sh
```

## Expanding beyond FEBio  
This repo can easily be modified to work with other command line processing software besides FEBio, but it involves knowing Docker, Python, and Condor, and requires a basic understanding of `generate_from_directory.py`. To use it with other software:  
- Change the Dockerfile such that it installs the needed software in the image (e.g. if you're running MatLab, modify the Dockerfile so that it installs MatLab).  
- Modify `generate_from_directory.py` so that `script_file` contains a command line argument to run the command line software. To feed in parameters, use `$1`.  
- Modify the `generate_job` function in `generate_from_directory.py` so that it has the correct input/output names and redirects output correcty.

### To do:  
- Make a user friendly method of submitting jobs - perhaps a web server with Node.js/React.js?
- Create documentation for submitting jobs from other machines if the central manager is not easily accessible.
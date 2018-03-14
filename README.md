# Finite Element Analysis with High Throughput Computing

My project at the biomechatronics lab at the MIT Media Lab in March 2018. Setting up a cluster of computers for high throughput computing to run prosthetics simulations.

The `generate_condor_job.py` script creates two files: a script for FEBio, and a job submission file for condor. The script simply looks like this (the FEBio location may need to be changed - change it by modifying the `FEBIO_LOCATION` variable in the Python script):  
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

Once these two files are created, move them to the same directory as the .feb file. Check that the Condor cluster is active with `condor_status`, and if it is, simply run `condor_submit <submission file>.sub` and wait for the cluster to run the analysis.

### TODO: 
- Create a job generator that iterates through an entire directory and generates jobs for Condor

# Installation and Initialization

To start a HTCondor network, you need two things: 1) a central manager, and 2) execution machines. Jobs are submitted to the central manager, and the central manager distributes jobs to the execution machines. 

- Clone this repository with `git clone https://github.com/kevin-fang/high-throughput-febio`
- Create a `condor_config.local` file in the repo's directory. Take a look at [sample_condor_config.local](sample_condor_config.local) for an example. In `condor_config.local`, you only need to change CONDOR_HOST to the IP address of the central manager.

For more customization, you might want to change the slot types and DAEMON_LIST.

For more instructions on creating `condor_config.local`, see [setting condor_config.local](#user-content-setting-condor_configlocal).  

Once the condor configuration file is created, follow one of these two methods:

### Initializing through Docker  
(Tested on Linux; might work on Windows. Doesn't work on Mac.)  
- Install [Docker](https://www.docker.com/) on your machine. 
- Add your user to the Docker group (`sudo usermod -aG docker <your username>`)
- Create a `condor_config.local` file.
- Run `./run_docker.sh /absolute/path/to/condor_config.local` to add your machine to the network. For example, to run a Docker container using the sample condor config file, you would run `./run_docker.sh /path/to/high-throughput-febio/sample_condor_config.local`. It will take some time to download the Docker image and initialize. Once it says "Starting Condor... done", then the machine will take about 20 seconds to add to the condor network.
- To remove your machine from the network and stop the docker image, run `./stop_docker.sh`
- To run on startup, add `cd /absolute/path/to/this/directory && ./run_docker.sh <condor config file>` to `/etc/rc.local` (Linux only) on your machine. 

### Native Installation  
(Linux only)  
- For Ubuntu/Debian: install HTCondor with `sudo apt-get install htcondor` For other Linux distros, you may need to [build from source](https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki). When installing, **select "no"** when "Manage installation of HTCondor automatically" appears. 
- Move the `condor_config.local` file to `/etc/condor/condor_config.local`  
- Start the condor instance with `sudo /etc/init.d/condor start`
- Stop the condor instance with `sudo /etc/init.d/condor stop`
- To restart the condor instance after changing the config file, run `sudo /etc/init.d/condor restart`
- To run on startup, you'll want to add `sudo /etc/init.d/condor start` to the `/etc/rc.local` file.

## Creating a central manager  
Instructions for creating a central manager are the same as adding a new machine to the network. The IP address that you include in the `condor_config.local` files should be the IP address of this computer. Once that's set up, do the following:
- Follow either the Docker or native installation instructions. 
- If you don't want your central manager to execute jobs, add the following line to your `condor_config.local`:  
`DAEMON_LIST = COLLECTOR, MASTER, NEGOTIATOR, SCHEDD`.
- **IMPORTANT**: Make sure that in the `condor_config.local` of your central manager, the DAEMON_LIST has `SCHEDD` and `NEGOTIATOR` present.

The central manager should be a computer with very high uptime, ideally one that is always on. When the central manager is restarted, all the execution nodes have to be restarted too. If for some reason the condor instance itself needs to be restarted on the central manager, run `condor_restart -all` on the central manager. 

If the central manager (CM) needs to be shut down or restarted, run `condor_status -master -format "%s\n" MasterIpAddr > addresses.txt` on the CM. his will save the IP addresses and the ports of all the execution nodes in a file called `addresses.txt`  
- To restart the CM: shut down/reboot/whatever on the CM, and then run ``condor_restart `cat addresses.txt` ``
- To shutdown the entire network, run ``condor_off `cat addresses` ``

## Adding a machine just to submit jobs  
If your central manager isn't your personal computer,  you probably want to be able to submit jobs without transferring files. Luckily, the process for creating a machine *just* for job submission is very simple. On the machine:  
- Create the `condor_config.local` file to the specification aboveand move it to `/etc/condor/condor_config.local`. This time, however, change the `DAEMON_LIST` variable to `DAEMON_LIST = MASTER, SCHEDD`
- Follow the *native* installation directions for Condor. Move the `condor_config.local` file to `/etc/condor/condor_config.local` and then run `/etc/init.d/condor restart`
- Submit jobs with `condor_submit <file>.sub`
- If you want to submit jobs through a Docker installation, the process becomes a little more convoluted, as it involves mounting volumes. Please look at the [Docker volume documentation](https://docs.docker.com/storage/volumes/#start-a-container-with-a-volume) for more instructions. You'll basically want to mount the project folder to somewhere in the Docker image by modifying the `run_docker.sh` script to mount an entire directory rather than a `condor_config.local` file.Then, use `docker exec condor_docker condor_submit <volume>` to submit jobs after starting the image with `run_docker.sh`

## Verifying the installation

Under `condor_status`, every machine with the correct `condor_config.local` settings should appear. For example:
```
Name               OpSys      Arch   State     Activity LoadAv Mem   ActvtyTime

slot1@medialab-1Ma LINUX      X86_64 Unclaimed Idle      1.000 2256  0+00:59:41
slot2@medialab-1Ma LINUX      X86_64 Unclaimed Idle      1.000 2256  0+01:00:05
slot3@medialab-1Ma LINUX      X86_64 Unclaimed Idle      0.130 2256  0+01:00:06
slot4@medialab-1Ma LINUX      X86_64 Unclaimed Idle      0.000 2256  0+01:00:07
slot5@medialab-1Ma LINUX      X86_64 Unclaimed Idle      0.000 2256  0+01:00:08
slot6@medialab-1Ma LINUX      X86_64 Unclaimed Idle      0.000 2256  0+01:00:09
slot7@medialab-1Ma LINUX      X86_64 Unclaimed Idle      0.000 2256  0+01:00:10
slot8@medialab-1Ma LINUX      X86_64 Unclaimed Idle      0.000 2256  0+01:00:03
slot1@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+00:08:41
slot2@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.010  996  0+01:00:05
slot3@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+01:00:06
slot4@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+01:00:07
slot5@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+01:00:08
slot6@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+01:00:09
slot7@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+01:00:10
slot8@medialab-3Ma LINUX      X86_64 Unclaimed Idle      0.000  996  0+01:00:03
                     Total Owner Claimed Unclaimed Matched Preempting Backfill

        X86_64/LINUX    16     0       0        16       0          0        0

               Total    16     0       0        16       0          0        0
```

### Setting condor_config.local

CONDOR_HOST points to the IP address of the central manager. DAEMON_LIST is configured as follows:  

- `MASTER` should *always* be present on every machine. It starts and controls the rest of the daemons.  
- `STARTD` is added if you wish for the machine to be able to execute jobs
- `SCHEDD` is added if you wish for the machine to be able to submit jobs
- `COLLECTOR` is only present on the central manager. It collects "ads" from the nodes that contain the specs of the nodes  
- `NEGOTIATOR` is only present on the central manager. It takes the scheduled jobs and "negotiates" which jobs to send to which nodes.

## Daemon Configurations

Machine just for executing jobs: `DAEMON_LIST = MASTER, STARTD`  
Just for submitting jobs: `DAEMON_LIST = MASTER, SCHEDD`  
To submit and execute jobs: `DAEMON_LIST = MASTER, STARTD, SCHEDD`  
Central manager: `DAEMON_LIST = MASTER, COLLECTOR, NEGOTIATOR, SCHEDD (optional: STARTD if you want your central manager to execute jobs)`

### Choosing specifications for nodes  

To set the specs on each machine, modify `/etc/condor/condor_config.local` with the following settings (by default the machine will evenly divide its RAM among its CPUS and create a machine on HTCondor for each):

If you wish to limit the resources to give to Condor, you must follow this section.

Define slot types like so:  
`SLOT_TYPE_<NUM> = cpus=<number of cpus>, ram=<amount of ram>, disk=<amount of disk space>`

You can set an arbitrary number of slot types. To make a machine with 4 CPU cores, 8 GB RAM, and 4 GB HDD space, add this to the config:  
`SLOT_TYPE_1 = cpus=4, ram=8192, disk=4096`

If there were 2 CPU cores and 2 GB RAM remaining, you would add:  
`SLOT_TYPE_2 = cpus=2, ram=2048` to the local config.

Once slot types are defined, in the same file `condor_config.local` define how much of each slot type will be available on the network with `NUM_SLOTS_TYPE_<NUM>`:

For example, for the machine above you would include:  
```
NUM_SLOTS_TYPE_1 = 1
NUM_SLOTS_TYPE_2 = 1
```

In total, the section of the config would look like this:  
```
SLOT_TYPE_1 = cpus=4, ram=8192, disk=4096
SLOT_TYPE_2 = cpus=2, ram=2048
NUM_SLOTS_TYPE_1 = 1
NUM_SLOTS_TYPE_2 = 1
```

When defining slot types, you can also use fractions or percentages:
```
SLOT_TYPE_1 = cpus=25%, ram=1/4, disk=10%
NUM_SLOTS_TYPE_1 = 1/4
```

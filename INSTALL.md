# Installation and Initialization

To start a HTCondor network, you need two things: 1) a central manager, and 2) execution machines. Jobs are submitted to the central manager, and the central manager distributes jobs to the execution machines. 

## Adding a machine to an existing network
- First, create a `condor_config.local` file in this directory, to the following specification (take a look at [sample_condor_config.local](sample_condor_config.local) for an example):  
```
CONDOR_HOST = <central manager's ip address - e.g. 192.168.0.101>
ALLOW_WRITE = <network of ip addresses - e.g. 192.168.0.*. Can also just be *>
ALLOW_NEGOTIATOR = $(CONDOR_HOST)
ALLOW_NEGOTIATOR_SCHEDD = $(ALLOW_NEGOTIATOR)
HOSTALLOW_CONFIG = $(CONDOR_HOST)
CONDOR_ADMIN = <user on the central manager machine - e.g. medialab@192.168.0.101>
NEGOTIATOR_HOST = $(CONDOR_HOST)
``` 

For more instructions on creating `condor_config.local`, see [setting condor_config.local](#user-content-setting-condor_configlocal).  

Once the condor configuration file is created, follow one of these two methods

### Initializing through Docker (Any OS - easier for those on macOS/Windows):  
- Install [Docker](https://www.docker.com/) on any machine (Linux, Windows, Mac). 
- Run `./run_docker.sh <name of config file, e.g. condor_config.local>` to add your machine to the network. For example, to run a Docker container using the sample condor config file, you would run `./run_docker.sh sample_condor_config.local`. It will take some time to initialize.
- To remove your machine from the network and stop the docker image, run `./stop_docker.sh`
- To run on startup, add the `cd /absolute/path/to/this/directory && ./run_docker.sh <condor config file>` to `/etc/rc.local` (Linux only) on your machine. 

### Native Installation (Linux only):  
- For Ubuntu/Debian: install HTCondor with `sudo apt-get install htcondor` For other Linux distros, you may need to [build from source](https://htcondor-wiki.cs.wisc.edu/index.cgi/wiki). When installing, ignore the prompts for filesystems, etc. 
- Move the `condor_config.local` file to `/etc/condor/condor_config.local`  
- Start the condor instance with `sudo /etc/init.d/condor start`
- Stop the condor instance with `sudo /etc/init.d/condor stop`
- To restart the condor instance after changing the config file, run `sudo /etc/init.d/condor restart`
- To run on startup, you'll want to add `sudo /etc/init.d/condor start` to the `/etc/rc.local` file.

## Creating a central manager  
Instructions for creating a central manager are the same as adding a new machine to the network. The IP address that you include in the `condor_config.local` files should be the IP address of this central computer. Once that's set up, do the following:
- Follow either the Docker or native installation instructions.
- If you don't want your central manager to execute jobs, add the following line to your `condor_config.local`:  
`DAEMON_LIST = COLLECTOR, MASTER, NEGOTIATOR, SCHEDD`.

The central manager should be a computer with very high uptime, ideally one that is always on. When the central manager is restarted, all the execution nodes have to be restarted too. If for some reason the condor instance itself needs to be restarted on the central manager, run `condor_restart -all` on the central manager. 

If the central manager (CM) needs to be shut down or restarted, run `condor_status -master -format "%s\n" MasterIpAddr > addresses.txt` on the CM. his will save the IP addresses and the ports of all the execution nodes in a file called `addresses.txt`  
- To restart the CM: shut down/reboot/whatever on the CM, and then run ``condor_restart `cat addresses.txt` ``
- To shutdown the entire network, run ``condor_off `cat addresses` ``

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

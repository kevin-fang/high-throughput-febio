# Installation and Initialization

### Installing through Docker (preferred method, much easier):  
- Install Docker on any machine (Linux, Windows, Mac).  
- Run `git clone https://github.com/kevin-fang/high-throughput-febio` and navigate to the `docker_install` directory.  
- In the `Dockerfile`, modify the line `wget --output-document=condor_config.local https://raw.githubusercontent.com/kevin-fang/high-throughput-febio/master/sample_condor_config.local` so that it will points to a corrected condor_config.local from the internet (create your own condor_config.local so it follows the format below and upload it to Dropbox/Google Drive/another cloud hosting service). Note the condor configuration file cannot be changed after you build the docker image. You can always rebuild the image with a corrected file, though.  
- Build the docker image with `docker build -t condor .`. After it finishes (it will take a few minutes), run `docker images` and check that there is an image present called "condor".  
- Run `docker run -itd --name=condor_docker condor /bin/bash && docker exec condor_docker /etc/init.d/condor start`. 
- To stop the container, run `docker exec condor_docker /etc/init.d/condor stop && docker kill condor_docker`.
- To automatically run condor every time your computer turns on, add the start command to `/etc/rc.local` (on Linux ) on *your* machine. For 

### Native Installation:  
Install the basic package with `sudo apt-get install htcondor`. Modify `/etc/condor/condor_config.local` to have the following text:

```
CONDOR_HOST = <host ip address - e.g. 192.168.0.101>
ALLOW_WRITE = <network of ip addresses - e.g. 192.168.0.*>
ALLOW_NEGOTIATOR = $(CONDOR_HOST)
ALLOW_NEGOTIATOR_SCHEDD = $(ALLOW_NEGOTIATOR)
HOSTALLOW_CONFIG = $(CONDOR_HOST)
CONDOR_ADMIN = <user on the root machine - e.g. root@192.168.0.101>
NEGOTIATOR_HOST = $(CONDOR_HOST)
``` 

Restart the condor instance with `sudo /etc/init.d/condor restart`. Under `condor_status`, every machine with the correct `condor_config.local` settings should appear. For example:
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

To set the specs on each machine, modify `/etc/condor/condor_config.local` with the following settings (by default the machine will evenly divide its RAM among its CPUS and create a machine on HTCondor for each):

Define slot types like so:  
`SLOT_TYPE_<NUM> = cpus=<number of cpus>, ram=<amount of ram>, disk=<amount of disk space>`. 

You can set an arbitrary number of slot types. To make a machine with 4 CPU cores, 8 GB RAM, and 4 GB HDD space, add this to the config:  
`SLOT_TYPE_1 = cpus=4, ram=8192, disk=4096`.

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
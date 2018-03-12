## How to install HTCondor on new machines

Install the basic package with `sudo apt-get install htcondor`. Modify `/etc/condor/condor_config.local` to have the following text:

```
CONDOR_HOST = <host ip address - e.g. 192.168.0.101>
ALLOW_WRITE = <network of ip addresses - e.g. 192.168.0.*>
FLOCK_FROM = <network of ip addresses - e.g. 192.168.0.*>
FLOCK_TO = <network of ip addresses - e.g. 192.168.0.*>
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

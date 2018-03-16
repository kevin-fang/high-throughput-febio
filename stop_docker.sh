#!/bin/sh
docker exec condor_docker /etc/init.d/condor stop && docker kill condor_docker
#!/bin/sh
docker rm -f condor_docker
docker pull kfang1233/condor:latest
docker run -itd --name=condor_docker -v $1:/condor_config.local kfang1233/condor /bin/bash
docker exec condor_docker cp /condor_config.local /etc/condor/condor_config.local
docker exec condor_docker /etc/init.d/condor start
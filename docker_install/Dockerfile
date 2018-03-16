FROM ubuntu:latest
MAINTAINER Kevin Fang <kevinzfang@gmail.com>
USER root
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get upgrade -y

RUN apt-get install htcondor -y

RUN apt-get install wget -y && \
    apt-get install unzip -y && \
    wget --output-document=febio.zip https://www.dropbox.com/s/55sgm0zoj1tlu3t/febio-2.6.4.zip?dl=1 && \
    unzip febio.zip
FROM ubuntu:latest
MAINTAINER FlowerYang <acheing.com>

RUN apt-get update
RUN apt-get -y install cron
RUN apt-get clean

RUN mkdir AutoPunch
ADD Daka /AutoPunch
ADD requirements.txt /AutoPunch


RUN apt-get -y install python3
RUN apt-get -y install python3-pip
RUN pip3 install -r /AutoPunch/requirements.txt


ADD run.sh /AutoPunch/run.sh
RUN echo '1 16 * * * sh /AutoPunch/run.sh 2>> /AutoPunch/run.log' > con
RUN crontab con
RUN rm con

CMD bash -c '/etc/init.d/cron start';'bash'

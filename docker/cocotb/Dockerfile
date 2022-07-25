FROM ubuntu:20.04

ARG NJOBS=5
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update
RUN apt-get -qq install python3 python3-pip git bison flex gperf libreadline5 libncurses5-dev autoconf

RUN rm -rf /var/cache/apt/archives

RUN pip install --upgrade pip
RUN pip install cocotb pytest ipython cocotb-test pytest-cov pytest-xdist bitstring pytest-lazy-fixture


RUN git clone https://github.com/steveicarus/iverilog
WORKDIR iverilog
RUN sh autoconf.sh && ./configure && make -j${NJOBS} && make install
WORKDIR ../
RUN rm -r iverilog

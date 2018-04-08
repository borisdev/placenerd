FROM ubuntu:14.04

RUN apt-get update && apt-get install -y build-essential \
	curl \
	libssl-dev \
	openssl \
	python-dev \
	python-pip \
	python-setuptools \
	vim \
	wget

ENV PATH /opt/miniconda/bin:$PATH
RUN wget http://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/miniconda && \
    rm miniconda.sh && \
    hash -r && \
    conda config --set always_yes yes --set changeps1 yes && \
    conda update -q conda

RUN conda install -c conda-forge ipython
RUN conda install -c conda-forge ipdb 
RUN conda install -c conda-forge numpy
RUN conda install -c conda-forge nltk
RUN pip install boto3==1.4.4

RUN apt-get update && apt-get install -y git
ADD ./ /opt

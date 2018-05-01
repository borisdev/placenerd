FROM ubuntu:14.04

RUN apt-get update && apt-get install -y \
        build-essential \
        curl \
        git \
        libapache2-mod-wsgi \
        libblas-dev \
        liblapack-dev \
        libssl-dev \
        apache2 \
        lsof \
        openssl \
        python-dev \
        python-pip \
        python-setuptools \
        vim \
        wget \
        mongodb-clients \
        sqlite3

RUN pip install uwsgi

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
RUN conda install -c anaconda pandas
RUN conda install -c conda-forge pytables
RUN pip install cenpy
RUN pip install pysal
RUN pip install mysql-connector==2.1.6
RUN pip install Django==1.11.2
RUN pip install djangorestframework==3.6.3
RUN pip install django-axes==2.3.2
RUN pip install requests==2.18.4
RUN pip install lxml==4.1.1

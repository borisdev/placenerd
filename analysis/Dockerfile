FROM continuumio/miniconda3
RUN pip install cenpy
RUN conda install -c conda-forge jupyter
#RUN apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN apt-get update && apt-get install -y vim 
RUN apt-get update && apt-get install -y wget
RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y tmux
RUN pip install ipdb

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
RUN pip install psycopg2
RUN pip install django-environ

RUN pip install pytz==2018.4  # https://github.com/stub42/pytz
RUN pip install awesome-slugify==1.6.5  # https://github.com/dimka665/awesome-slugify
RUN pip install Pillow==5.1.0  # https://github.com/python-pillow/Pillow
RUN pip install argon2-cffi==18.1.0  # https://github.com/hynek/argon2_cffi
RUN pip install redis>=2.10.5  # https://github.com/antirez/redis

# Django
# ------------------------------------------------------------------------------
#RUN pip install django==2.0.4  # pyup: < 2.1  # https://www.djangoproject.com/
RUN pip install django-environ==0.4.4  # https://github.com/joke2k/django-environ
RUN pip install django-model-utils==3.1.1  # https://github.com/jazzband/django-model-utils
RUN pip install django-allauth==0.35.0  # https://github.com/pennersr/django-allauth
RUN pip install django-crispy-forms==1.7.2  # https://github.com/django-crispy-forms/django-crispy-forms
RUN pip install django-redis==4.9.0  # https://github.com/niwinz/django-redis

# Django REST Framework
RUN pip install djangorestframework==3.8.2  # https://github.com/encode/django-rest-framework
RUN pip install coreapi==2.3.3  # https://github.com/core-api/python-client

RUN pip install Werkzeug==0.14.1  # https://github.com/pallets/werkzeug
RUN pip install ipdb==0.11  # https://github.com/gotcha/ipdb
RUN pip install Sphinx==1.7.4  # https://github.com/sphinx-doc/sphinx
RUN pip install psycopg2==2.7.4 --no-binary psycopg2  # https://github.com/psycopg/psycopg2

# Testing
# ------------------------------------------------------------------------------
RUN pip install pytest==3.5.1  # https://github.com/pytest-dev/pytest
RUN pip install pytest-sugar==0.9.1  # https://github.com/Frozenball/pytest-sugar

# Code quality
# ------------------------------------------------------------------------------
RUN pip install flake8==3.5.0  # https://github.com/PyCQA/flake8
RUN pip install coverage==4.5.1  # https://github.com/nedbat/coveragepy

# Django
# ------------------------------------------------------------------------------
RUN pip install factory-boy==2.10.0  # https://github.com/FactoryBoy/factory_boy
RUN pip install django-test-plus==1.0.22  # https://github.com/revsys/django-test-plus

RUN pip install django-debug-toolbar==1.9.1  # https://github.com/jazzband/django-debug-toolbar
RUN pip install django-extensions==2.0.7  # https://github.com/django-extensions/django-extensions
RUN pip install django-coverage-plugin==1.5.0  # https://github.com/nedbat/django_coverage_plugin
RUN pip install pytest-django==3.2.1  # https://github.com/pytest-dev/pytest-django

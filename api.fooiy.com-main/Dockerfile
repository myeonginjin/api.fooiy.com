############################################################
# Dockerfile to run a Django-based fooiy RESTful SEVER
# Based on an AMI
############################################################

# Set base image
FROM ubuntu:20.04

# Set maintainer
LABEL name="fooiy"

# Directory in container for all project files
ENV FOOIY_DOCKER_SRVHOME=/srv
# Local directory with project source
ENV FOOIY_DOCKER_SRC=repo
# Directory in container for project source files
ENV FOOIY_DOCKER_SRVPROJ=$FOOIY_DOCKER_SRVHOME/$FOOIY_DOCKER_SRC

# Set TImezone
ENV TZ='Asia/Seoul'
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set apt packages
RUN apt-get -y update
RUN apt-get install -y python3-pip python3-dev
RUN apt-get install -y apt-utils
RUN apt-get install -y tzdata
RUN cd /usr/local/bin
RUN ln -s /usr/bin/python3 python
RUN pip3 install --upgrade pip
RUN apt-get install -y libssl-dev
RUN apt-get install -y mysql-server
RUN apt-get install -y libmysqlclient-dev
RUN apt-get install -y git
RUN apt-get install -y vim
RUN apt-get install -y nginx
RUN apt-get install --reinstall -y systemd
RUN pip3 install gunicorn
RUN pip3 install gevent

# SET Locale
RUN apt-get install -y language-pack-ko
RUN locale-gen ko_KR.UTF-8

# SET openssl.cnf
COPY $FOOIY_DOCKER_SRC/openssl.cnf /usr/lib/ssl/openssl.cnf

# Create application LogDir
WORKDIR $FOOIY_DOCKER_SRVHOME
RUN mkdir logs
# Log Mount
VOLUME ["$FOOIY_DOCKER_SRVHOME/logs/"]

# Copy application source code to SRCDIR
COPY $FOOIY_DOCKER_SRC/requirements.txt $FOOIY_DOCKER_SRVPROJ/requirements.txt

# Install Python dependencies
RUN pip3 install -r $FOOIY_DOCKER_SRVPROJ/requirements.txt

# ENV setting
ARG PHASE \
    DJANGO_SECRET_KEY \
    AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY \
    DATABASES_DEFAULT_HOST \
    DATABASES_PRODUCTION_HOST \
    DATABASES_DEFAULT_NAME \
    DATABASES_DEFAULT_USER \
    DATABASES_DEFAULT_PASSWORD \
    DEV_DATABASES_DEFAULT_HOST \
    DEV_DATABASES_DEFAULT_NAME \
    DEV_DATABASES_DEFAULT_USER \
    DEV_DATABASES_DEFAULT_PASSWORD \
    CACHES_DEFAULT_HOST \
    DEV_CACHES_DEFAULT_HOST \
    SLACK_TOKEN \
    EMAIL_HOST_USER \
    EMAIL_HOST_PASSWORD \
    FOOIY_JWT_SECRET_KEY \
    FOOIY_WEB_TOKEN \
    FOOIY_GUEST_TOKEN

ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8 \
    PHASE=$PHASE \
    DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY \
    AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
    DATABASES_DEFAULT_HOST=$DATABASES_DEFAULT_HOST \
    DATABASES_PRODUCTION_HOST=$DATABASES_PRODUCTION_HOST \
    DATABASES_DEFAULT_NAME=$DATABASES_DEFAULT_NAME \
    DATABASES_DEFAULT_USER=$DATABASES_DEFAULT_USER \
    DATABASES_DEFAULT_PASSWORD=$DATABASES_DEFAULT_PASSWORD \
    DEV_DATABASES_DEFAULT_HOST=$DEV_DATABASES_DEFAULT_HOST \
    DEV_DATABASES_DEFAULT_NAME=$DEV_DATABASES_DEFAULT_NAME \
    DEV_DATABASES_DEFAULT_USER=$DEV_DATABASES_DEFAULT_USER \
    DEV_DATABASES_DEFAULT_PASSWORD=$DEV_DATABASES_DEFAULT_PASSWORD \
    CACHES_DEFAULT_HOST=$CACHES_DEFAULT_HOST \
    DEV_CACHES_DEFAULT_HOST=$DEV_CACHES_DEFAULT_HOST \
    SLACK_TOKEN=$SLACK_TOKEN \
    EMAIL_HOST_USER=$EMAIL_HOST_USER \
    EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD \
    FOOIY_JWT_SECRET_KEY=$FOOIY_JWT_SECRET_KEY \
    FOOIY_WEB_TOKEN=$FOOIY_WEB_TOKEN \
    FOOIY_GUEST_TOKEN=$FOOIY_GUEST_TOKEN

#COPY sources
COPY $FOOIY_DOCKER_SRC/manage.py $FOOIY_DOCKER_SRVPROJ/manage.py
COPY $FOOIY_DOCKER_SRC/accounts $FOOIY_DOCKER_SRVPROJ/accounts
COPY $FOOIY_DOCKER_SRC/archives $FOOIY_DOCKER_SRVPROJ/archives
COPY $FOOIY_DOCKER_SRC/common $FOOIY_DOCKER_SRVPROJ/common
COPY $FOOIY_DOCKER_SRC/feeds $FOOIY_DOCKER_SRVPROJ/feeds
COPY $FOOIY_DOCKER_SRC/fooiy $FOOIY_DOCKER_SRVPROJ/fooiy
COPY $FOOIY_DOCKER_SRC/shops $FOOIY_DOCKER_SRVPROJ/shops
COPY $FOOIY_DOCKER_SRC/static $FOOIY_DOCKER_SRVPROJ/static
COPY $FOOIY_DOCKER_SRC/templates $FOOIY_DOCKER_SRVPROJ/templates
COPY $FOOIY_DOCKER_SRC/ui $FOOIY_DOCKER_SRVPROJ/ui
COPY $FOOIY_DOCKER_SRC/web $FOOIY_DOCKER_SRVPROJ/web
COPY $FOOIY_DOCKER_SRC/firebase_service_account_key.json $FOOIY_DOCKER_SRVPROJ/firebase_service_account_key.json

# Port to expose
EXPOSE 80

WORKDIR $FOOIY_DOCKER_SRVPROJ
COPY ./django_nginx.conf /etc/nginx/sites-available/
RUN ln -s /etc/nginx/sites-available/django_nginx.conf /etc/nginx/sites-enabled
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

# Run Server
COPY ./docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]
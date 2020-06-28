FROM tiangolo/uvicorn-gunicorn:python3.7

LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir fastapi
COPY ./app /app
#
#     SSH - Begin Part #1
#
ENV SSH_PASSWD "root:Docker!"
ENV SSH_PORT 2222

#Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        openssh-server \
        vim \
        curl \
        wget \
        tcptraceroute \
    && pip install --upgrade pip \      
	&& echo "$SSH_PASSWD" | chpasswd 

COPY sshd_config /etc/ssh/
COPY init_container.sh /usr/local/bin/

RUN chmod u+x /usr/local/bin/init_container.sh \
     && echo "$SSH_PASSWD" | chpasswd \
     && echo "cd /usr/local/bin" >> /etc/bash.bashrc
#
#     SSH - End Part #1
#
RUN chmod 755 /mnt  \
     && echo "$SSH_PASSWD" | chpasswd \
     && echo "cd /mnt" >> /etc/bash.bashrc

RUN chmod 755 /opt  \
     && echo "$SSH_PASSWD" | chpasswd \
     && echo "cd /opt" >> /etc/bash.bashrc

WORKDIR /app

RUN pip install -r ./requirements.txt

#
#     SSH - Begin Part #2
#

EXPOSE 8081 2222
#
#     SSH - End Part #2
#
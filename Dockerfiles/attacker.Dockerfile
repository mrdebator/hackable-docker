FROM phusion/baseimage:master

LABEL name="attacker"

RUN apt update -y \
    && apt install -y \
    nmap \
    git \
    net-tools \
    iputils-ping \
    curl \
    proxychains4 \
    ncat \
    hydra \
    && git clone https://github.com/danielmiessler/SecLists.git /opt/seclists
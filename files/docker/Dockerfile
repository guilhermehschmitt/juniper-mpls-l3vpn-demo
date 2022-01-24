FROM python:slim-buster

### -------------------------------------------------
### Metadata information
### -------------------------------------------------
LABEL name="juniper-mpls-l3vpn-demo"
LABEL maintainer="cremsburg.dev@gmail.com"
LABEL description="Python container to test automation with"
LABEL license="GPLv3"
LABEL url="https://github.com/cdot65/juniper-mpls-l3vpn-demo"
LABEL build-date="20220135"

### -------------------------------------------------
### Change directory to /tmp/files
### -------------------------------------------------
WORKDIR /tmp/files

### -------------------------------------------------
### Add and install python packages
### -------------------------------------------------
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install --upgrade pip

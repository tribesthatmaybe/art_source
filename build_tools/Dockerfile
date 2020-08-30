FROM fedora:32

MAINTAINER 'ttmb dev <info@tribesthatmay.be>'
ARG VERSION=0.0.0
LABEL version="${VERSION}"

RUN dnf -y install python2 gimp

# Have to do this hack because gimp still runs off of Python 2.
# might poke at that, don't know how tightly integrated that is
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python2 get-pip.py
RUN pip2 install toml

COPY export_maps.py /usr/lib/python2.7/site-packages/

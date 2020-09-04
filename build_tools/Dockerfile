FROM fedora:32

MAINTAINER 'ttmb dev <info@tribesthatmay.be>'
ARG VERSION=0.0.0
LABEL version="${VERSION}"

RUN dnf -y install python2 gimp

# Have to do this hack because gimp still runs off of Python 2.
# might poke at that, don't know how tightly integrated that is
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python2 get-pip.py
RUN pip2 install wheel

COPY tribes_art_build_tools-13-py2-none-any.whl /tmp/
RUN pip2 install /tmp/tribes_art_build_tools-13-py2-none-any.whl
RUN pip2 show -f tribes_art_build_tools

COPY entrypoint.sh /usr/local/bin/ttmb-texture-entrypoint
RUN chmod +rx /usr/local/bin/ttmb-texture-entrypoint

# Once I build something for models (eh?) this might become
# multipurpose and need something to handle when to do what
ENTRYPOINT ["ttmb-texture-entrypoint"]

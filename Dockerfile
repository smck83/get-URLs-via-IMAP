FROM python:3.9
LABEL maintainer="s@mck.la"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ntp \
    && mkdir -p /opt/clickurls \
    && pip install requests
ADD main.py /opt/clickurls

WORKDIR /opt/clickurls


VOLUME ["/opt/clickurls"]

ENTRYPOINT python -u /opt/clickurls/main.py


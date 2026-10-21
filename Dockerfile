# Every module is a compiled extension built for CPython 3.12 on x86-64 Linux
# (glibc 2.39), so the base image is pinned to Ubuntu 24.04.
FROM ubuntu:24.04

ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends python3.12 python3-pip python3.12-venv \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN python3.12 -m venv /opt/venv \
 && /opt/venv/bin/pip install --no-cache-dir --upgrade pip \
 && /opt/venv/bin/pip install --no-cache-dir .

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /work

ENTRYPOINT ["pokerskill-agent"]
CMD ["--help"]

FROM ubuntu:noble

RUN apt-get update \
    && apt-get -qqy install \
    bc \
    sudo \
    build-essential \
    ca-certificates \
    curl \
    gcc \
    git \
    vim \
    openssh-server \
    clang-format \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    python3-setuptools \
    virtualenv \
    libsqlite3-dev \
    srecord \
    udev \
    xz-utils \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

USER $USERNAME

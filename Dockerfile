FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    python3 \
    python3-dev \
    python3-pip \
    openjdk-17-jdk \
    autoconf \
    libtool \
    pkg-config \
    libncurses5-dev \
    libncursesw5-dev \
    libtinfo5 \
    cmake \
    libffi-dev \
    libssl-dev \
    automake \
    zip \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip setuptools wheel

RUN pip3 install \
    kivy \
    kivy-deps.angle \
    kivy-deps.glew \
    kivy-deps.sdl2 \
    pyjnius \
    buildozer \
    beautifulsoup4 \
    requests \
    cython

WORKDIR /app

COPY . /app/

RUN buildozer android init

CMD ["buildozer", "android", "debug"]

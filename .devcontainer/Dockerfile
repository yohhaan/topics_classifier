FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 \
    python3-pip \
    protobuf-compiler \
    libusb-1.0-0-dev \
    git \
    parallel \
    locales \
    wget && \
    apt-get clean autoclean && \
    apt-get autoremove
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8
ENV LANG en_US.UTF-8
RUN pip3 install --break-system-packages --upgrade pip && \
    pip3 install --break-system-packages black numpy pandas Pyarrow tflite-support
RUN addgroup --gid 1000 vscode
RUN adduser --disabled-password --gecos "" --uid 1000 --gid 1000 vscode
ENV HOME /home/vscode
USER vscode


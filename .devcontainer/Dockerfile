FROM debian:latest
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y python3 \
    python3-pip \
    protobuf-compiler \
    libusb-1.0-0-dev \
    git \
    wget && \
    apt-get clean autoclean && \
    apt-get autoremove
RUN pip3 install --break-system-packages --upgrade pip && \
    pip3 install --break-system-packages black numpy pandas Pyarrow tflite-support
RUN addgroup --gid 1000 vscode
RUN adduser --disabled-password --gecos "" --uid 1000 --gid 1000 vscode
ENV HOME /home/vscode
USER vscode


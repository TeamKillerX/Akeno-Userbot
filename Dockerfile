FROM rendyprojects/python:latest

RUN apt -qq update && \
    apt -qq install -y --no-install-recommends \
    ffmpeg \
    curl \
    git \
    gnupg2 \
    unzip \
    wget \
    python3-dev \
    python3-pip \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    neofetch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

WORKDIR /usr/src/app

RUN chown -R 1000:0 /usr/src/app \
    && chown -R 1000:0 . \
    && chmod 777 . \
    && chmod 777 /usr \
    && chown -R 1000:0 /usr

COPY . .
RUN pip3 install --upgrade pip setuptools==59.6.0
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5
RUN md5sum -c ffmpeg-git-amd64-static.tar.xz.md5
RUN tar xvf ffmpeg-git-amd64-static.tar.xz
RUN mv ffmpeg-git*/ffmpeg ffmpeg-git*/ffprobe /usr/local/bin/

EXPOSE 7860

# Run the application
CMD ["bash", "-c", "python3 server.py & python3 -m Akeno"]

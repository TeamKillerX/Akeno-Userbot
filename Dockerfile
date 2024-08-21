FROM rendyprojects/python:latest

WORKDIR /app
WORKDIR /.cache

RUN apt -qq update && \
    apt -qq install -y --no-install-recommends \
    ffmpeg \
    curl \
    git \
    gnupg2 \
    unzip \
    wget \
    xvfb \
    libxi6 \
    libgconf-2-4 \
    libappindicator3-1 \
    libxrender1 \
    libxtst6 \
    libnss3 \
    libatk1.0-0 \
    libxss1 \
    fonts-liberation \
    libasound2 \
    libgbm-dev \
    libu2f-udev \
    libvulkan1 \
    libgl1-mesa-dri \
    xdg-utils \
    python3-dev \
    python3-pip \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavfilter-dev \
    libavutil-dev \
    libswscale-dev \
    libswresample-dev \
    chromium \
    chromium-driver \
    neofetch && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/

RUN mkdir -p /tmp/ && \
    cd /tmp/ && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    dpkg -i ./google-chrome-stable_current_amd64.deb; apt -fqqy install && \
    rm ./google-chrome-stable_current_amd64.deb

RUN mkdir -p /tmp/ && \
    cd /tmp/ && \
    wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip && \
    unzip -o /tmp/chromedriver.zip chromedriver -d /usr/bin/ && \
    rm /tmp/chromedriver.zip

ENV CHROME_DRIVER /usr/bin/chromedriver
ENV CHROME_BIN /usr/bin/google-chrome-stable

COPY . .
COPY requirements.txt .
RUN pip3 install --upgrade pip setuptools==59.6.0
RUN pip3 install -r requirements.txt

RUN chown -R 1000:0 .
RUN chmod 777 .
RUN chown -R 1000:0 /app
RUN chmod 777 /app
RUN chown -R 1000:0 /.cache
RUN chmod 777 /.cache

RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5
RUN md5sum -c ffmpeg-git-amd64-static.tar.xz.md5
RUN tar xvf ffmpeg-git-amd64-static.tar.xz
RUN mv ffmpeg-git*/ffmpeg ffmpeg-git*/ffprobe /usr/local/bin/

EXPOSE 7860

CMD ["bash", "-c", "python3 server.py & python3 -m Akeno"]

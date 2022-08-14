FROM ros:noetic

WORKDIR /root/Downloads

COPY . .

RUN apt update && apt-get install -y python3-pip \
    git \
    libjpeg-dev \
    libpng-dev \
    ffmpeg  \
    libsm6  \
    libxext6

RUN python3 -m pip install ouster-sdk tqdm bsdf opencv-python pillow

WORKDIR /tmp

RUN git clone https://github.com/LASzip/LASzip.git && \
    cd LASzip && \
    cmake . && \
    make && \
    make install && \
    pip install laspy[lazrs,laszip] pypcd open3d

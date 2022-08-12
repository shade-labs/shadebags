FROM ros:noetic

WORKDIR /root/Downloads

COPY . .

RUN apt update && apt-get install -y python3-pip

RUN python3 -m pip install pillow ouster-sdk tqdm bsdf opencv-python

RUN apt update &&  \
    apt install -y \
        git \
        libjpeg-dev \
        libpng-dev

WORKDIR /tmp
RUN git clone https://github.com/LASzip/LASzip.git && \
    cd LASzip && \
    cmake . && \
    make && \
    make install && \
    pip install laspy[lazrs,laszip]

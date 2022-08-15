FROM ros:noetic-perception

RUN apt update && apt install -y \
    ros-noetic-ros-numpy \
    libpcl-dev

WORKDIR /root/Downloads

COPY . .

RUN apt update && apt-get install -y python3-pip git

RUN python3 -m pip install ouster-sdk tqdm pillow

WORKDIR /tmp

RUN git clone https://github.com/LASzip/LASzip.git && \
    cd LASzip && \
    cmake . && \
    make && \
    make install && \
    pip install laspy[lazrs,laszip] pypcd open3d open3d-ros-helper # python-pcl

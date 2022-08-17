FROM ros:noetic-perception

WORKDIR /root/Downloads

COPY . .

RUN apt update && apt-get install -y  \
    python3-pip \
    git \
    wget \
    ros-noetic-ros-numpy

RUN python3 -m pip install ouster-sdk tqdm pillow

WORKDIR /tmp

RUN wget https://github.com/PointCloudLibrary/pcl/archive/refs/tags/pcl-1.9.1.tar.gz && \
    tar -zxvf pcl-1.9.1.tar.gz && \
    cd pcl-pcl-1.9.1 && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install

RUN git clone https://github.com/LASzip/LASzip.git && \
    cd LASzip && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make && \
    make install && \
    pip install laspy[lazrs,laszip] pypcd open3d open3d-ros-helper python-pcl

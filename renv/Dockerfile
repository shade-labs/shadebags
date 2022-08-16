FROM ros:noetic-perception

RUN apt update && apt install -y \
    ros-noetic-ros-numpy

WORKDIR /root/Downloads

COPY . .

RUN apt update && apt-get install -y python3-pip git

RUN python3 -m pip install ouster-sdk tqdm pillow

WORKDIR /tmp

RUN curl https://github.com/PointCloudLibrary/pcl/archive/refs/tags/pcl-1.9.1.tar.gz && \
    tar xvfj pcl-pcl-1.9.1.tar.gz && \
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

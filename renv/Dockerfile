FROM ros:noetic

WORKDIR /root/Downloads

COPY ./stairs_compressed.bag .

RUN apt update && apt-get install -y python3-pip

RUN python3 -m pip install pillow tqdm bsdf

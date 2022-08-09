FROM ros:noetic

WORKDIR /root/Downloads

COPY . .

RUN apt update && apt-get install -y python3-pip

RUN python3 -m pip install pillow ouster-sdk laspy tqdm bsdf

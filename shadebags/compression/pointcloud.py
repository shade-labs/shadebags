import os
import laspy
import shutil
from ouster import client, pcap
from ouster.sdk.examples import pcap as converter

import numpy as np
import rospy
import roslib
import sensor_msgs.point_cloud2 as pc2
import open3d as o3d
import ctypes
import struct


class PC:
    def __init__(self):
       self.__warned_disk = False

    @staticmethod
    def compress(metadata, data):
        data = pc2.create_cloud(metadata, metadata, data)

        gen = pc2.read_points(data, skip_nans=True)
        int_data = list(gen)
        xyz = np.empty((len(int_data), 3))
        rgb = np.empty((len(int_data), 3))

        for x in int_data:
            test = x[3]
            # cast float32 to int so that bitwise operations are possible
            s = struct.pack('>f', test)
            i = struct.unpack('>l', s)[0]
            # you can get back the float value by the inverse operations
            pack = ctypes.c_uint32(i).value
            r = (pack & 0x00FF0000) >> 16
            g = (pack & 0x0000FF00) >> 8
            b = (pack & 0x000000FF)

        out_pcd = o3d.geometry.PointCloud()
        out_pcd.points = o3d.utility.Vector3dVector(xyz)
        out_pcd.colors = o3d.utility.Vector3dVector(rgb)
        o3d.io.write_point_cloud("./", out_pcd)
        print("finishing")



if __name__ == "__main__":

    # download from https://ouster.com/resources/lidar-sample-data/
    pcap_path = '/root/Downloads/data.pcap'
    metadata_path = '/root/Downloads/config.json'

    with open(metadata_path, 'r') as f:
        info = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, info)

    directory = './tmp'
    os.mkdir(directory)
    os.mkdir('./final')

    # convert pcap to las
    converter.pcap_to_las(source=source, metadata=info, las_dir=directory)

    # convert las to laz
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        las = laspy.read(f)
        las.write(f'./final/{filename[:-4]}.laz')

    shutil.make_archive('example.shade', 'zip', 'final')
    shutil.rmtree(directory)
    shutil.rmtree('./final')
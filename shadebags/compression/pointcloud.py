import os
import laspy
import shutil
from ouster import client, pcap
from ouster.sdk.examples import pcap as converter

import ros_numpy
import numpy as np
import pypcl
from open3d_ros_helper import open3d_ros_helper as orh
import open3d as o3d

class PC:
    def __init__(self):
       self.__warned_disk = False

    @staticmethod
    def compress(metadata, data):
        pc = ros_numpy.numpify(data)
        points = np.zeros((pc.shape[0], 3))
        points[:, 0] = pc['x']
        points[:, 1] = pc['y']
        points[:, 2] = pc['z']
        p = pcl.PointCloud(np.array(points, dtype=np.float32))

        # print("running")
        # o3dpc = orh.rospc_to_o3dpc(data)
        # print("modified")
        # o3d.io.write_point_cloud('test.pcd', o3dpc)
        # print("saved?")



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
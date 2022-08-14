import os
import laspy
import shutil
from ouster import client, pcap
from ouster.sdk.examples import pcap as converter

from sensor_msgs.msg import PointCloud2
class PC:
    def __init__(self):
       self.__warned_disk = False

    @staticmethod
    def compress(metadata, data):
        print(metadata, data)



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
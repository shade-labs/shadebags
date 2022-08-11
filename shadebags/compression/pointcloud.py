import os
import laspy
# fromt .compression import LazBackend
from ouster import client, pcap
from ouster.sdk.examples import pcap as converter

if __name__ == "__main__":

    # download from https://ouster.com/resources/lidar-sample-data/
    pcap_path = '/root/Downloads/OS1.pcap'
    metadata_path = '/root/Downloads/osconfig.json'

    with open(metadata_path, 'r') as f:
        info = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, info)

    directory = './tmp'
    # convert pcap to las
    # converter.pcap_to_las(source=source, metadata=info, las_dir=directory)

    # convert las to laz
    for filename in os.listdir('./tmp'):
        f = os.path.join('./tmp', filename)

        las = laspy.read(f)
        las.write(f'./final/{filename[:-4]}.laz')
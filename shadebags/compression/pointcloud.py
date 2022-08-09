import io
from ouster import client, pcap
from ouster.sdk.examples import pcap as converter

if __name__ == "__main__":

    # download from https://ouster.com/resources/lidar-sample-data/
    pcap_path = '/root/Downloads/OS1.pcap'
    metadata_path = '/root/Downloads/osconfig.json'

    with open(metadata_path, 'r') as f:
        info = client.SensorInfo(f.read())

    source = pcap.Pcap(pcap_path, info)

    # convert pcap to las
    converter.pcap_to_las(source=source, metadata=info)

    # for packet in source:
    #     if isinstance(packet, client.LidarPacket):
    #         # Now we can process the LidarPacket. In this case, we access
    #         # the measurement ids, timestamps, and ranges
    #         measurement_ids = packet.measurement_id
    #         timestamps = packet.timestamp
    #         ranges = packet.field(client.ChanField.RANGE)
    #         print(f'  encoder counts = {measurement_ids.shape}')
    #         print(f'  timestamps = {timestamps.shape}')
    #         print(f'  ranges = {ranges.shape}')
    #
    #     elif isinstance(packet, client.ImuPacket):
    #         # and access ImuPacket content
    #         print(f'  acceleration = {packet.accel}')
    #         print(f'  angular_velocity = {packet.angular_vel}')
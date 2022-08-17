from shadebags.writer import Writer
from shadebags.defaults import BagDefaults
import rosbag
from shadebags.compression.pointcloud import PC

if __name__ == "__main__":
    input = '/root/Downloads/pointcloud.bag'
    output = './'

    # compressor = PC()
    #
    # input_bag = rosbag.Bag(input)
    # for topic, msg, t in input_bag.read_messages():
    #     print(msg)
    #     compressor.compress("yikes", msg)

    #
    writer = Writer(input, output, BagDefaults.ROS1)
    writer.write()
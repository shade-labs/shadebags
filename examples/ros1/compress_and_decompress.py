import os
import time

import shadebags

input_path = '/root/Downloads/stairs_compressed.bag'
output_dir = '/root/Downloads'

if __name__ == "__main__":
    # Create some folders to store the outputs
    os.mkdir('/root/Downloads/compressed')
    os.mkdir('/root/Downloads/decompressed')

    # Write the shadebag
    writer = shadebags.Writer(input_path, '/root/Downloads/compressed', shadebags.types.ROS1)
    writer.write()

    # Read the shadebag back to a rosbag
    reader = shadebags.Reader(f'/root/Downloads/compressed/stairs_compressed.shade', '/root/Downloads/decompressed', shadebags.types.ROS1)
    reader.read()

    print("Done")

    time.sleep(1000000000)

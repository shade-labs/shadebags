import time

import shade

input_path = '/root/Downloads/stairs_compressed.bag' # '../../renv/stairs_compressed.bag'  # '/root/Downloads/stairs_compressed.bag'
output_path = '/root/Downloads/output.shade'

if __name__ == "__main__":
    writer = shade.Writer(input_path, output_path, shade.types.ROS1)

    writer.write()

    time.sleep(1000000000)

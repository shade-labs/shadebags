# This file will write a bag file (/root/Downloads/stairs_compressed.bag) -
#  to a compressed shade file (/root/Downloads/stairs_compressed.shade)

import shadebags

input_path = '/root/Downloads/stairs_compressed.bag'

if __name__ == "__main__":
    writer = shadebags.Writer(input_path, '/root/Downloads', shadebags.types.ROS1)
    writer.write()

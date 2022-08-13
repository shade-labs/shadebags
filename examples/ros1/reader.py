# This file will read a compressed shade file (/root/Downloads/stairs_compressed.shade) -
#  to a ros bag file (/root/Downloads/stairs_compressed.bag)

import shadebags

input_path = '/root/Downloads/stairs_compressed.shade'

if __name__ == "__main__":
    reader = shadebags.Reader(input_path, '/root/Downloads', shadebags.types.ROS1)
    reader.read()

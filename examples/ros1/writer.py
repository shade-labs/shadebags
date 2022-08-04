import shade

input_path = '~/Downloads/rooftop_ouster.bag'
output_path = '~/Downloads'

if __name__ == "__main__":
    writer = shade.Writer(input_path, output_path, shade.types.ROS1)

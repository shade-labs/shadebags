import io

from PIL import Image


class JPG:
    def __init__(self, points):
        self.image = Image.open(io.BytesIO(image))

    @staticmethod
    def compress(self) -> bytes:
        buf = io.BytesIO()
        self.image.save(buf, format='JPEG')
        jpeg_bytes = buf.getvalue()
        return jpeg_bytes


import rosbag

if __name__ == "__main__":
    input_bag = rosbag.Bag('/root/Downloads/stairs_compressed.bag')

    for topic, msg, t in input_bag.read_messages():
        print(f'Topic: {topic} \n'
              f'Msg  : {str(msg)[0:100]} \n'
              f'Time : {t}')

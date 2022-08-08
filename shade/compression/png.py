import io
import random

from PIL import Image


class PNG:
    def __init__(self, format_, width, height, image: bytes):
        self.og = image
        self.image = Image.frombytes(format_, (width, height), image, 'raw')
    
    def compress(self) -> bytes:
        buf = io.BytesIO()
        # self.image.save(buf, format='PNG')
        self.image.save(f'/root/Downloads/{random.randint(0, 1000)}.png', format='PNG')
        png_bytes = buf.getvalue()
        return png_bytes

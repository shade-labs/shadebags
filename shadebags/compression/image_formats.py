import io

from PIL import Image


class PNG:
    def __init__(self, format_, width, height, image: bytes):
        self.og = image
        self.image = Image.frombytes(format_, (width, height), image, 'raw')
    
    def compress(self) -> bytes:
        buf = io.BytesIO()
        self.image.save(buf, format='PNG')
        png_bytes = buf.getvalue()
        return png_bytes


class JPEG:
    def __init__(self, format_, width, height, image: bytes):
        self.og = image
        self.image = Image.frombytes(format_, (width, height), image, 'raw')

    def compress(self) -> bytes:
        buf = io.BytesIO()
        self.image.save(buf, format='JPEG')
        png_bytes = buf.getvalue()
        return png_bytes

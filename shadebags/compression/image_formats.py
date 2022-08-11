import io

from PIL import Image


class PNG:
    def __init__(self):
        pass

    @staticmethod
    def compress(format_, width, height, image: bytes) -> bytes:
        buf = io.BytesIO()
        Image.frombytes(format_, (width, height), image, 'raw').save(buf, format='PNG')
        png_bytes = buf.getvalue()
        return png_bytes

    @staticmethod
    def decompress(format_, width, height, image: bytes) -> bytes:
        buf = io.BytesIO()
        Image.frombytes(format_, (width, height), image, 'PNG').save(buf, format='raw')
        png_bytes = buf.getvalue()
        return png_bytes


class JPEG:
    def __init__(self):
        pass

    @staticmethod
    def compress(format_, width, height, image: bytes) -> bytes:
        buf = io.BytesIO()
        Image.frombytes(format_, (width, height), image, 'raw').save(buf, format='JPEG')
        jpeg_bytes = buf.getvalue()
        return jpeg_bytes

    @staticmethod
    def decompress(format_, width, height, image: bytes) -> bytes:
        buf = io.BytesIO()
        Image.frombytes(format_, (width, height), image, 'JPEG').save(buf, format='raw')
        jpeg_bytes = buf.getvalue()
        return jpeg_bytes

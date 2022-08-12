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
        input_buf = io.BytesIO(image)
        output_buf = io.BytesIO()
        Image.open(input_buf, formats=('png',)).save(output_buf, format_='raw')
        raw_bytes = output_buf.getvalue()
        return raw_bytes


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
        input_buf = io.BytesIO(image)
        output_buf = io.BytesIO()
        Image.open(input_buf, formats=('jpeg',)).save(output_buf,  format_='raw')
        raw_bytes = output_buf.getvalue()
        return raw_bytes

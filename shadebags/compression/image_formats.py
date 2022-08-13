import io
import os

from PIL import Image
import uuid
import warnings

class PNG:
    def __init__(self):
        self.__warned_disk = False

    @staticmethod
    def compress(format_, width, height, image: bytes) -> bytes:
        buf = io.BytesIO()
        Image.frombytes(format_, (width, height), image, 'raw').save(buf, format='PNG')
        png_bytes = buf.getvalue()
        return png_bytes

    def decompress(self, format_, width, height, image: bytes) -> bytes:
        input_buf = io.BytesIO(image)

        if not self.__warned_disk:
            warnings.warn("Decoding error, using disk IO instead of buffer.")
            self.__warned_disk = True

        filename = str(uuid.uuid4())

        input_tmp = open(f'{filename}.png', 'wb')
        input_tmp.write(input_buf.getvalue())
        input_tmp.close()

        output_buf = io.BytesIO(Image.open(f'./{filename}.png').tobytes())

        os.remove(f'./{filename}.png')
        return output_buf.getvalue()


class JPEG:
    def __init__(self):
        self.__warned_disk = False

    @staticmethod
    def compress(format_, width, height, image: bytes) -> bytes:
        buf = io.BytesIO()
        Image.frombytes(format_, (width, height), image, 'raw').save(buf, format='JPEG')
        jpeg_bytes = buf.getvalue()
        return jpeg_bytes

    def decompress(self, format_, width, height, image: bytes) -> bytes:
        input_buf = io.BytesIO(image)

        if not self.__warned_disk:
            warnings.warn("Decoding error, using disk IO instead of buffer.")
            self.__warned_disk = True

        filename = str(uuid.uuid4())

        input_tmp = open(f'{filename}.jpeg', 'wb')
        input_tmp.write(input_buf.getvalue())
        input_tmp.close()

        output_buf = io.BytesIO(Image.open(f'./{filename}.jpeg').tobytes())

        os.remove(f'./{filename}.jpeg')
        return output_buf.getvalue()

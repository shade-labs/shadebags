import io

from PIL import Image


class JPG:
    def __init__(self, image):
        self.image = Image.open(io.BytesIO(image))
    
    @staticmethod
    def compress(self) -> bytes:
        buf = io.BytesIO()
        self.image.save(buf, format='JPEG')
        jpeg_bytes = buf.getvalue()
        return jpeg_bytes

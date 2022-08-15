"""
    Chooses a compression algorithm when available
    Copyright (C) 2022  Emerson Dove

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.
    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from shadebags.defaults import DataTypes
from .image_formats import PNG, JPEG
from .pointcloud import PC

class Compressor:
    def __init__(self):
        self.__jpeg = JPEG()
        self.__png = PNG()
        self.__pointcloud = PC()

    def compress(self, data: bytes, shade_type: DataTypes or None, metadata: dict = None):
        print(shade_type)
        if shade_type == DataTypes.image:
            if metadata['encoding'] == 'RGB':
                return self.__jpeg.compress(metadata['encoding'], metadata['width'], metadata['height'], data)
            else:
                return self.__png.compress(metadata['encoding'], metadata['width'], metadata['height'], data)

        if shade_type == DataTypes.pointcloud:
            return self.__pointcloud.compress(metadata, data)

    def decompress(self, data: bytes, shade_type: DataTypes or None, metadata: dict = None):
        if shade_type == DataTypes.image:
            if metadata['encoding'] == 'RGB':
                return self.__jpeg.decompress(metadata['encoding'], metadata['width'], metadata['height'], data)
            else:
                return self.__png.decompress(metadata['encoding'], metadata['width'], metadata['height'], data)

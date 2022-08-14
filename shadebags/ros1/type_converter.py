"""
    Maps ROS types to Shade types
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

import typing
from shadebags.defaults import DataTypes

class Decoder:
    def __init__(self):
        self.__warned_types = {}
        self.types = {
            'sensor_msgs/Image': self.__decode_image,
            'sensor_msgs/PointCloud2': self.__decode_pointcloud
        }

    def convert_type(self, ros_type: str, metadata: dict, body: bytes = None) -> (dict, typing.Any, DataTypes):
        try:
            return self.types[ros_type](body, metadata)
        except KeyError:
            if ros_type not in self.__warned_types:
                print(f"No conversion algorithm matching {ros_type}")
                self.__warned_types[ros_type] = True
            return metadata, body, DataTypes.none

    @staticmethod
    def __decode_image(data: bytes, metadata: dict) -> (dict, typing.Any, DataTypes):
        """
        ROS image types require no modification to be compatible with Shade compression
        :param data: ROS bytes input
        :return: Unmodified data
        """
        encoding_map: dict = {
            'mono16': 'I;16',
            'rgb8': 'RGB'
        }

        metadata['encoding'] = encoding_map[metadata['encoding']]
        return metadata, data, DataTypes.image

    @staticmethod
    def __decode_pointcloud(data: bytes, metadata: dict) -> (dict, typing.Any, DataTypes):
        return metadata, data, DataTypes.pointcloud

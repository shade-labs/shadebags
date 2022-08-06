"""
    Write data to the Shade format
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
import struct

from .defaults import BagDefaults
from rosbags.rosbag1 import Reader
# import rosbag


class Writer:
    def __init__(self, input_file: str, output_file: str, bag_type: BagDefaults):
        self.__input_file = input_file
        self.__output_file = output_file
        self.__bag_type = bag_type

    def write(self):
        if self.__bag_type == BagDefaults.ROS1:
            # for topic, msg, t in rosbag.Bag(self.__input_file).read_messages():
            #     print(f'Topic: {topic}\n'
            #           f'msg:   {str(msg)[0:1000]}')


            bag = Reader(self.__input_file)

            bag.open()

            for connection, timestamp, rawdata, header in bag.messages():
                print(f'Header: {type(header)}\n'
                      f'\tTime: {str(timestamp)} \n'
                      f'\tRaw : {str(rawdata)[0:1000]}')

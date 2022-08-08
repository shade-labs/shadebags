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


from .defaults import BagDefaults
from .compression.compressor import Compressor


class Writer:
    def __init__(self, input_file: str, output_file: str, bag_type: BagDefaults):
        self.__input_file = input_file
        self.__output_file = output_file
        self.__bag_type = bag_type
        self.__compressor = Compressor()

    def write(self):
        compressed_msgs = []
        if self.__bag_type == BagDefaults.ROS1:
            from .ros1.decoder import ROS1Decoder
            msgs = ROS1Decoder(self.__input_file).decode()
            for msg in msgs:
                if 'data' in msg.message:
                    print("has data")
                    msg.message['data'] = self.__compressor.compress(msg.message['data'],
                                                                     msg.message['type'],
                                                                     msg.message['meta'])
                compressed_msgs.append(msg)

            print("Compression completed")

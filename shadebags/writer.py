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
from tqdm import tqdm
import bsdf
import multiprocessing

MAX_CPUS = multiprocessing.cpu_count()


class Writer:
    def __init__(self, input_file: str, output_file: str, bag_type: BagDefaults):
        self.__input_file = input_file
        self.__output_file = output_file
        self.__bag_type = bag_type
        self.__compressor = Compressor()

    def compress(self, msg):
        if 'data' in msg.message:
            msg.message['data'] = self.__compressor.compress(msg.message['data'],
                                                             msg.message['type'],
                                                             msg.message['meta'])
        return msg

    def write(self):
        def convert_dict_to_bytes(dictionary: dict):
            for key in dictionary:
                pass


        compressed_msgs = []
        if self.__bag_type == BagDefaults.ROS1:
            from .ros1.decoder import ROS1Decoder
            msgs = ROS1Decoder(self.__input_file).decode()
            print(f'Compressing using {MAX_CPUS} CPUs...')
            pool = multiprocessing.Pool(processes=MAX_CPUS)
            for result in tqdm(pool.map(self.compress, msgs)):
                compressed_msgs.append(result)

            # Make sure everything is in the right order
            compressed_msgs.sort(key=lambda x: x.message['time'])
            print("Compression completed")

        raw_msgs = []

        with open(self.__output_file, 'wb') as output_file:
            print("Writing...")
            for msg in tqdm(compressed_msgs):
                # Convert the enum back to a string
                current_message = msg.message
                current_message['type'] = current_message['type'].value

                raw_msgs.append(current_message)

            output_file.write(bsdf.encode(raw_msgs))

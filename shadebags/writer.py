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
import os.path

from .defaults import BagDefaults
from .compression.compressor import Compressor
from tqdm import tqdm
import multiprocessing

MAX_CPUS = multiprocessing.cpu_count()


class Writer:
    def __init__(self, input_file: str, output_dir: str, bag_type: BagDefaults):
        if not os.path.isfile(input_file):
            raise LookupError(f"{input_file} does not reference a file")

        if not os.path.isdir(output_dir):
            raise LookupError(f"{output_dir} is not a directory")

        file_name = f'{os.path.basename(input_file).split(".")[0]}.shade'
        self.__input_file = input_file
        self.__output_file = os.path.join(output_dir, file_name)
        self.__bag_type = bag_type
        self.__compressor = Compressor()

    def compress(self, msg):
        if 'data' in msg.message:
            msg.message['data'] = self.__compressor.compress(msg.message['data'],
                                                             msg.message['type'],
                                                             msg.message['meta'])
        return msg

    def write(self):
        compressed_msgs = []
        if self.__bag_type == BagDefaults.ROS1:
            from .ros1.decoder import ROS1Decoder
            decoder = ROS1Decoder(self.__input_file, self.__output_file)
            msgs = decoder.decode()
            print(f'Compressing using {MAX_CPUS} CPUs...')
            pool = multiprocessing.Pool(processes=MAX_CPUS)
            for result in tqdm(pool.map(self.compress, msgs)):
                compressed_msgs.append(result)

            # Make sure everything is in the right order
            compressed_msgs.sort(key=lambda x: x.message['time'])
            print("Compression completed")

            # Easy
            decoder.write(compressed_msgs)

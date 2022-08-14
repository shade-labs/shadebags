"""
    Decompose the bag into Shade format
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
import copy
import os
from typing import List

from shadebags.abc_decoder import Decoder
from shadebags.shade_msg import ShadeMsg
from .type_converter import Decoder as TypeDecoder
import rosbag
import genpy
import subprocess
import shadebags.utils as utils


class ROS1Decoder(Decoder):
    def __init__(self, input_file, output_file):
        self.__input_file = input_file
        self.__output_file = output_file

    @staticmethod
    def __fix_time(headers):
        """
        Fix the header time to be a nice looking object
        :param headers: A ROS headers object, extracted from __extract_class_attributes
        :return: The headers with the nasty removed
        """
        time_key = 'stamp'
        # Confirm that 'stamp' is correct for this message
        if time_key in headers and isinstance(headers[time_key], genpy.Time):
            pass
        else:
            found = False
            for key in headers:
                if isinstance(headers[key], genpy.Time):
                    found = True
                    time_key = key

            if not found:
                raise LookupError("Could not find a time attribute in the message headers")

        # Get rid of nasty ros object
        headers[time_key] = headers[time_key].to_sec()

        return headers, headers[time_key]

    @staticmethod
    def __extract_class_attributes(obj) -> dict:
        """
        Extract the important attributes from the ROS class
        :param obj: Any input object
        :return: Return the attributes like 'width' instead of things like '__init__'
        """
        members = dir(obj)
        header_members = []
        for member in members:
            if member[0] != '_':
                if not callable(getattr(obj, member)):
                    header_members.append(member)

        header = {}
        for header_key in header_members:
            header[header_key] = getattr(obj, header_key)

        return header

    def decode(self) -> List[ShadeMsg]:
        def get_headers(ros_msg):
            try:
                message = self.__extract_class_attributes(ros_msg)
            except AttributeError:
                return

            return {
                'body': message,
            }

        extracted_messages = []

        input_bag = rosbag.Bag(self.__input_file)

        type_info = input_bag.get_type_and_topic_info().topics

        type_converter = TypeDecoder()

        for topic, msg, t in input_bag.read_messages():
            topic_copy = copy.deepcopy(topic)
            msg_copy = copy.deepcopy(msg)
            t_copy = copy.deepcopy(t)
            parsed = get_headers(msg)

            body = parsed.get('body', None)

            converted_data = {
                'topic': topic,
                'time': t,
            }

            if body is not None and 'data' in body:
                converted_data['data'] = body['data']
                body.pop('data')

                # Copy meta in
                converted_data['meta'] = body

                converted_data['meta'], converted_data['data'], converted_data['type'] = type_converter.convert_type(type_info[topic].msg_type,
                                                                                                                     converted_data['meta'],
                                                                                                                     converted_data['data'])
            else:
                # Body is turned into metadata
                if body is not None:
                    # Also copy meta in because you can have meta without data
                    converted_data['meta'] = body
                    converted_data['meta'], _, converted_data['type'] = type_converter.convert_type(type_info[topic].msg_type, converted_data['meta'])

            extracted_messages.append(ShadeMsg(converted_data,
                                               topic=topic_copy,
                                               msg=msg_copy,
                                               t=t_copy))

        return extracted_messages

    def write(self, compressed_data: List[ShadeMsg]):
        output_file = rosbag.Bag(self.__output_file, 'w')

        for shade_msg in compressed_data:
            topic = shade_msg.kwargs['topic']
            msg = shade_msg.kwargs['msg']
            t = shade_msg.kwargs['t']

            if 'data' in shade_msg.message:
                msg.data = shade_msg.message['data']
                output_file.write(topic, msg, t)
            else:
                output_file.write(topic, msg, t)


        print("Indexing shade output...")
        subprocess.check_output(f'rosbag reindex {self.__output_file}', shell=True)

        matches = utils.determine_backup_file(os.path.dirname(self.__output_file),
                                              os.path.basename(str(self.__output_file).split('.')[0]))

        if not len(matches) == 1:
            print("Could not remove backup file")
        else:
            # Remove the single backup file
            os.remove(os.path.join(os.path.dirname(self.__output_file), matches[0]))

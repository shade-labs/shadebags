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
from typing import List

from shadebags.abc_decoder import Decoder
from shadebags.shade_msg import ShadeMsg
from .type_converter import Decoder as TypeDecoder
import rosbag
import genpy


class ROS1Decoder(Decoder):
    def __init__(self, input_file):
        self.__input_file = input_file

    @staticmethod
    def __convert_types(ros_dict: dict):
        def __determine_if_valid_type(value):
            return isinstance(value, str) or isinstance(value, int) or isinstance(value, float)

        def __convert_type(value):
            pass

        for key in ros_dict:
            if not __determine_if_valid_type(ros_dict['key']):
                pass

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
                header = self.__extract_class_attributes(ros_msg.header)

            except AttributeError:
                return

            # Fix the header time
            header, time_ = self.__fix_time(header)

            # Make sure the header is removed from the message
            message.pop('header')

            return {
                'header': header,
                'body': message,
                'time': time_
            }

        extracted_messages = []

        input_bag = rosbag.Bag(self.__input_file)

        type_info = input_bag.get_type_and_topic_info().topics

        type_converter = TypeDecoder()

        for topic, msg, t in input_bag.read_messages():
            parsed = get_headers(msg)

            # Skip anything without a header
            if parsed is None:
                continue

            headers = parsed['header']
            body = parsed.get('body', None)
            time = parsed['time']

            converted_data = {
                'topic': topic,
                'time': time,
                'header': headers
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

            # Add the original type to the meta header
            if isinstance(converted_data['meta'], dict):
                converted_data['meta']['original_type'] = type_info[topic].msg_type
            else:
                converted_data['meta'] = {
                    'original_type': type_info[topic].msg_type
                }

            extracted_messages.append(ShadeMsg(converted_data))

        return extracted_messages

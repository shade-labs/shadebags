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


from shade.abc_decoder import Decoder
import rosbag
import genpy


class ROS1Decoder(Decoder):
    def __init__(self, input_file):
        self.__input_file = input_file

    def decode(self):
        def get_headers(ros_msg):
            try:
                members = dir(ros_msg.header)
                header_members = []
                for member in members:
                    if member[0] != '_':
                        if not callable(getattr(ros_msg.header, member)):
                            header_members.append(member)

                spec = ros_msg.header._spec
            except AttributeError:
                return

            header = {}
            for header_key in header_members:
                header[header_key] = getattr(ros_msg.header, header_key)

            header['spec'] = spec
            return header

        extracted_messages = []

        for topic, msg, t in rosbag.Bag(self.__input_file).read_messages():
            headers = get_headers(msg)

            # Skip anything without a header
            if headers is None:
                continue

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

            converted_data = {
                'topic': topic,
                'time': headers[time_key],
                'meta': headers,
            }

            if hasattr(msg, 'data'):
                converted_data['data'] = {
                    msg.data
                }
            extracted_messages.append(converted_data)

        return extracted_messages

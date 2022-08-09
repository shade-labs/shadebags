"""
    Default auto-conversion types
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


import enum


class BagDefaults(enum.Enum):
    ROS1 = 'ROS1'
    ROS2 = 'ROS2'
    MCAP = 'MCAP'

class DataTypes(enum.Enum):
    image = 'sensor_msgs/Image'
    pointcloud = 'sensor_msgs/Pointcloud'
    none = 'none'

"""
    Standard shade message format
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

from typing import TypedDict

class MsgFormat(TypedDict):
    topic: str
    time: int
    type: str
    header: dict
    data: typing.Any
    meta: dict

class ShadeMsg:

    def __init__(self, msg_dict: MsgFormat = None):
        self.__message = msg_dict

    @property
    def message(self) -> MsgFormat:
        if self.__message is None:
            raise LookupError("Never initialized with message")
        else:
            return self.__message

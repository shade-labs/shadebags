"""
    Common utilities
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
import os


def determine_backup_file(folder: str, base_name: str) -> list:
    files = os.listdir(folder)

    orig_files = []
    for file in files:
        if '.orig' in file:
            orig_files.append(file)

    matches = []
    for file in orig_files:
        if base_name in file:
            matches.append(file)

    return matches
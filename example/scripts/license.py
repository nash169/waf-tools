#!/usr/bin/env python
# encoding: utf-8

import fnmatch
import re
import os
import shutil
import sys


class License:
    license_text = {
        "mit": """
Copyright (c) 2019, 2020 Bernardo Fichera <bernardo.fichera@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
            """,

        "gnu": """
<one line to give the program's name and a brief idea of what it does.>
Copyright (C) 2020  Bernardo Fichera

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
                """,
    }

    def __init__(self, license="mit"):
        self.license = license

    # License getter/setter
    @property
    def license(self):
        return self.license_

    @license.setter
    def license(self, value):
        self.license_ = value

    # Insert license
    def insert(self, directory):
        # C/C++
        cpp = self.make_dirlist(directory, ['.hpp', '.cpp', '.h', '.c', '.cc'])
        for i in cpp:
            self.insert_header(i, '/*', '*/', self.license_text[self.license])

        # Python
        py = self.make_dirlist(directory, ['.py'])
        header = ['#!/usr/bin/env python', '# encoding: utf-8']
        for i in py:
            self.insert_header(
                i, '#', '', self.license_text[self.license], header)

        # CMake (metapackages should not have any comments)
        cmake = self.make_dirlist(directory, ['CMakeLists.txt'])
        for i in cmake:
            self.insert_header(i, '#', '', self.license_text[self.license])

        # XML/URDF
        xml_urdf = self.make_dirlist(
            directory, ['.xml', '.urdf', '.xacro', '.launch'])
        header = ['<?xml version="1.0"?>']

        for i in xml_urdf:
            self.insert_header(
                i, '<!--', '-->', self.license_text[self.license], header)

    def make_dirlist(self, folder, extensions):
        matches = []
        for root, _, filenames in os.walk(folder):
            for ext in extensions:
                for filename in fnmatch.filter(filenames, '*' + ext):
                    matches.append(os.path.join(root, filename))
        return matches

    def insert_header(self, fname, prefix, postfix, license, kept_header=[]):
        input = open(fname, 'r')
        ofname = '/tmp/' + fname.split('/')[-1]
        output = open(ofname, 'w')

        for line in kept_header:
            output.write(line + '\n')

        output.write(prefix + '\n')

        has_postfix = len(postfix) > 0

        my_prefix = prefix

        if has_postfix:
            my_prefix = ''
        for line in license.split('\n'):
            if len(line) > 0:
                output.write(my_prefix + '    ' + line + '\n')
            else:
                output.write(my_prefix + '\n')

        if has_postfix:
            output.write(postfix + '\n')

        in_header = False

        for line in input:
            header = len(
                list(filter(lambda x: x == line[0:len(x)], kept_header))) != 0
            check_prefix = (line[0:len(prefix)] == prefix)
            check_postfix = (has_postfix and (line[0:len(postfix)] == postfix))
            if check_prefix and has_postfix:
                in_header = True
            if check_postfix:
                in_header = False
            if (not in_header) and (not check_prefix) and (not header) and (not check_postfix):
                output.write(line)

        output.close()
        shutil.move(ofname, fname)

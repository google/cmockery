#!/usr/bin/python
#
# Copyright 2019 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for the `doc_gen` module."""

import unittest
import doc_gen


class ProcessFileTest(unittest.TestCase):

    def setUp(self):
        self.docgen_readfile = None


    def tearDown(self):
        if self.docgen_readfile is not None:
            doc_gen.ReadFileRaw = self.docgen_readfile


    def _setCustomReadFile(self, filepath_contents):
        self.docgen_readfile = doc_gen.ReadFileRaw
        def readFileCustom(filename):
            for filepath, contents in filepath_contents:
                if filename == filepath:
                    return contents
                else:
                    raise Exception('Expected file: "%s", received: "%s"' %
                            (filepath, filename))

        doc_gen.ReadFileRaw = readFileCustom


    def testPreC99Comments(self):
        source_file = 'file.c'
        source_file_fullpath = '/source/code/%s' % source_file
        marker = 'docs'
        source_file_contents = [
            '/* license header comment */\n',
            '\n',
            '/* BEGIN: %s */\n' % marker,
            '#include <stdio.h>\n',
            '/* END: %s */\n' % marker,
            'int main(int argc, char** argv) {\n',
            '  return 0;\n',
            '}\n',
        ]

        md_file_path = 'file.md.in'
        md_file_contents = [
            'text before code\n',
            '{{"source": "%s", "marker": "%s"}}\n' % (source_file_fullpath, marker),
            'text after code\n',
        ]

        expected_output = [
            'text before code\n',
            '[`%s`](%s)\n' % (source_file, source_file_fullpath),
            '\n',
            '~~~c\n',
            '#include <stdio.h>\n',
            '~~~\n',
            'text after code\n',
        ]

        self._setCustomReadFile(
                [(source_file_fullpath, source_file_contents),
                 (md_file_path, md_file_contents)])
        actual_output = list(doc_gen.ProcessFile(md_file_contents))
        self.assertEquals(expected_output, actual_output)


    def testC99Comments(self):
        source_file = 'file.c'
        source_file_fullpath = '/source/code/%s' % source_file
        marker = 'docs'
        source_file_contents = [
            '/* license header comment */\n',
            '\n',
            '// BEGIN: %s\n' % marker,
            '#include <stdio.h>\n',
            '// END: %s\n' % marker,
            'int main(int argc, char** argv) {\n',
            '  return 0;\n',
            '}\n',
        ]

        md_file_path = 'file.md.in'
        md_file_contents = [
            'text before code\n',
            '{{"source": "%s", "marker": "%s"}}\n' % (source_file_fullpath, marker),
            'text after code\n',
        ]

        expected_output = [
            'text before code\n',
            '[`%s`](%s)\n' % (source_file, source_file_fullpath),
            '\n',
            '~~~c\n',
            '#include <stdio.h>\n',
            '~~~\n',
            'text after code\n',
        ]

        self._setCustomReadFile(
                [(source_file_fullpath, source_file_contents),
                 (md_file_path, md_file_contents)])
        actual_output = list(doc_gen.ProcessFile(md_file_path))
        self.assertEquals(expected_output, actual_output)


if __name__ == '__main__':
    unittest.main()

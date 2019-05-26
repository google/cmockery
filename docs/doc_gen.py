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

"""Processes a Markdown file with source code include directives and outputs a
Markdown file with source code substitution and syntax highlighting
directives."""

import argparse
import json
import os
import re
import sys


def ReadFileRaw(filename):
    """Reads the entire file, emits each line separately."""
    with open(filename, 'r') as source:
        for line in source:
            yield line


def ReadFileContentsWithMarker(filename, marker):
    """Processes given file, returns lines surrounded by marker."""
    begin_comment_c = re.compile(r'^/\* BEGIN: (\w+) \*/$')
    end_comment_c = re.compile(r'^/\* END: (\w+) \*/$')
    begin_comment_cpp = re.compile(r'^// BEGIN: (\w+)$')
    end_comment_cpp = re.compile(r'^// END: (\w+)$')

    def Matches(matcherA, matcherB, content):
        return (matcherA.match(content), matcherB.match(content))

    def Valid(matches):
        return matches[0] or matches[1]

    def Group1(matches):
        if matches[0]:
            return matches[0].group(1)
        else:
            return matches[1].group(1)

    output = False
    for line in ReadFileRaw(filename):
        begin_matches = Matches(begin_comment_c, begin_comment_cpp, line)
        if Valid(begin_matches):
            begin_marker = Group1(begin_matches)
            if begin_marker == marker:
                yield '~~~c\n'  # Markdown C formatting header
                output = True
                continue        # avoid outputting our own begin line

        end_matches = Matches(end_comment_c, end_comment_cpp, line)
        if Valid(end_matches):
            end_marker = Group1(end_matches)
            if end_marker == marker:
                yield '~~~\n'  # Markdown formatting end block
                return         # we are done with this region

        if output:
            yield line  # enables outputting nested region markers


def ProcessFile(headerTpl, filename):
    """Process a Markdown file for source code includes.

    Returns:
      a line-at-a-time generator, replacing markers with source code
    """
    for line in headerTpl(filename):
        yield line

    pattern = re.compile(r'^{({.*})}$')
    for line in ReadFileRaw(filename):
        match = pattern.match(line)
        if not match:
            yield line
            continue

        # Handle special include
        params = json.loads(match.group(1))
        full_path = params['source']
        base_name = os.path.basename(full_path)
        yield '[`%s`](%s)\n' % (base_name, full_path)
        yield '\n'
        marker = params['marker']
        for item in ReadFileContentsWithMarker(full_path, marker):
            yield item


def ProcessFilesToStdout(headerTpl, sources):
    """Processes file, prints results to stdout."""
    for source in sources:
        results = ProcessFile(headerTpl, source)
        for line in results:
            sys.stdout.write('%s' % line)


def ProcessFilesInPlace(headerTpl, sources):
    """Processes Markdown file for includes, writes each output to disk.

    Each input file is assumed to have a `.in` suffix; this is stripped and the
    resulting name is used as the output filename.
    """
    for source in sources:
        output = source.rstrip('.in')
        with open(output, 'w') as dest:
            results = ProcessFile(headerTpl, source)
            for line in results:
                dest.write('%s' % line)


def DiffFiles(headerTpl, sources):
    """Compares expected output from processing to existing on-disk file.

    Generates output in-memory; compares the received output with contents of a
    file on disk. Compares the two line-by-line, if any diff is found, only the
    first diff is returned.

    Returns:
      (bool, string): if no diff: (True, None); otherwise, (False, diff error)
    """
    for source in sources:
        on_disk_file = source.rstrip('.in')
        on_disk_contents = list(ReadFileRaw(on_disk_file))

        results = ProcessFile(headerTpl, source)
        results_contents = list(results)

        if len(on_disk_contents) != len(results_contents):
            return False, ('Diff: %s (%d lines) vs. %s (%d lines)\n' %
                    (on_disk_file, len(on_disk_contents),
                     '<output>', len(results_contents)))

        for index, lines in enumerate(zip(on_disk_contents, results_contents)):
            if lines[0] != lines[1]:
                return False, ('Diff on line %d:\n'
                               '- %s'
                               '+ %s' % (index + 1, lines[0], lines[1]))

    return True, None


def main(argv):
    parser = argparse.ArgumentParser(
            description='Process Markdown files to include code samples.')
    parser.add_argument('-d', dest='diff', action='store_true',
            default=False, help='diff existing files vs. planned output')
    parser.add_argument('-w', dest='overwrite', action='store_true',
            default=False, help='overwrite files in-place')
    parser.add_argument('files', metavar='filename', type=str, nargs='+',
            help='filenames to process; must end with ".in" suffix')

    args = parser.parse_args()

    if args.diff and args.overwrite:
        sys.stderr.write('Cannot specify both -d and -w in a single run\n')
        sys.exit(1)

    for filename in args.files:
        if not filename.endswith('.in'):
            sys.stderr.write('Filename must end with ".in": %s\n' % filename)
            sys.exit(1)

    def headerTpl(filename):
        yield '<!-- This file was auto-generated by `%s %s`.\n' % (
                argv[0], filename)
        yield '     Do not modify manually; changes will be overwritten. -->\n'
        yield '\n'

    if args.diff:
        ok, error = DiffFiles(headerTpl, args.files)
        if not ok:
            sys.stderr.write('%s' % error)
            sys.exit(1)
    elif args.overwrite:
        ProcessFilesInPlace(headerTpl, args.files)
    else:
        ProcessFilesToStdout(headerTpl, args.files)


if __name__ == '__main__':
    main(sys.argv)

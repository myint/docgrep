#!/usr/bin/env python
#
# Copyright (C) 2014 Steven Myint
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""grep through docstrings only."""

from __future__ import (absolute_import,
                        division,
                        print_function,
                        unicode_literals)

import io
import os
import signal
import sys
import tokenize


__version__ = '0.1'


try:
    unicode
except NameError:
    unicode = str


def grep(source, search_term):
    """Yield matches in the form ((line, column), string)."""
    sio = io.StringIO(source)
    previous_token_type = None
    only_comments_so_far = True

    for (token_type,
         token_string,
         start,
         _,
         __) in tokenize.generate_tokens(sio.readline):

        if (
            token_type == tokenize.STRING and
            token_string.startswith(('"', "'")) and
            (previous_token_type == tokenize.INDENT or only_comments_so_far)
        ):
            if search_term in token_string:
                yield (start, token_string)

        if token_type not in [tokenize.COMMENT, tokenize.NEWLINE, tokenize.NL]:
            only_comments_so_far = False

        previous_token_type = token_type


def open_with_encoding(filename, encoding, mode='r'):
    """Return opened file with a specific encoding."""
    return io.open(filename, mode=mode, encoding=encoding,
                   newline='')  # Preserve line endings


def detect_encoding(filename):
    """Return file encoding."""
    try:
        with open(filename, 'rb') as input_file:
            from lib2to3.pgen2 import tokenize as lib2to3_tokenize
            encoding = lib2to3_tokenize.detect_encoding(input_file.readline)[0]

            # Check for correctness of encoding.
            with open_with_encoding(filename, encoding) as input_file:
                input_file.read()

        return encoding
    except (SyntaxError, LookupError, UnicodeDecodeError):
        return 'latin-1'


def grep_file(filename, args, standard_out):
    """Run grep() on a file."""
    encoding = detect_encoding(filename)
    with open_with_encoding(filename, encoding=encoding) as input_file:
        source = input_file.read()
        for start, docstring in grep(source, args.search_term):
            print('{}:{}: {}'.format(filename, start[0], docstring),
                  file=standard_out)


def _main(argv, standard_out, standard_error):
    """Internal main entry point."""
    import argparse
    parser = argparse.ArgumentParser(description=__doc__, prog='docgrep')
    parser.add_argument('--version', action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('search_term',
                        help='term to search for')
    parser.add_argument('paths', nargs='*',
                        help='paths to search')

    args = parser.parse_args(argv[1:])

    if not args.paths:
        args.paths = '.'

    filenames = list(set(args.paths))
    while filenames:
        name = filenames.pop(0)
        if os.path.isdir(name):
            for root, directories, children in os.walk(unicode(name)):
                filenames += [os.path.join(root, f) for f in children
                              if f.endswith('.py') and
                              not f.startswith('.')]
                directories[:] = [d for d in directories
                                  if not d.startswith('.')]
        else:
            try:
                grep_file(name, args=args, standard_out=standard_out)
            except IOError as exception:
                print(unicode(exception), file=standard_error)


def main():
    """Main entry point."""
    try:
        # Exit on broken pipe.
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:  # pragma: no cover
        # SIGPIPE is not available on Windows.
        pass

    try:
        return _main(sys.argv,
                     standard_out=sys.stdout,
                     standard_error=sys.stderr)
    except KeyboardInterrupt:
        return 2  # pragma: no cover


if __name__ == '__main__':
    sys.exit(main())

# coding: utf-8
'''
The MIT License (MIT)

Copyright (c) 2014 Andreas "Akki" Nitsch

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

class TextElement:
    """Class holding information of text-elements and their text."""
    # pylint: disable-msg=R0903
    # pylint: disable-msg=R0913
    def __init__(self, identifier, text, filename, metainfo, index=""):
        """Constructor.

            @param identifier: ID of text-element given by Custom Control id in mockup-file..
            @param text: text contained in mockup-element
            @param filename: name of mockup-file from that text was extracted.
            @param metainfo: meta-information givem by Custom Control data in mockup.
        """
        self.identifier = identifier
        self.text = text
        self.filename = filename
        self.meta = metainfo
        self.index = index

    def __eq__(self, other):
        """Method that checks if two instances of this class are equal."""
        if self.identifier != other.identifier or self.text != other.text or self.meta != other.meta or self.index != other.index:
            return False
        return True

    def __lt__(self, other):
        """ Method used for sorting text-elements for export in output-file."""
        return self.filename < other.filename
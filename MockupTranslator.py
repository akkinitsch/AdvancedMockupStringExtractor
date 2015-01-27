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


"""This module containes a class that is used to extract texts from balsamiq-mockup-files and to write them
into XML-files that can be used as input for translation-memory-systems.
"""

__version__ = "1.0.3"

import argparse
import glob
import logging
import os
import re
import sys

from lxml import etree

from OutputExporter import OutputExporter
from TextElement import TextElement
from TextFormatFixer import TextFormatFixer

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class MockupTranslator():
    """Class handling the extracting-process of text from Mockup-files."""

    texts = []
    """List with all recognized text in balsamiq-objects."""


    def __init__(self, input_file_dir=None, input_translation=None):
        self.readTranslation(input_translation)

    def readTranslation(self, input_file):
        logging.info("Extracting text from file " + input_file)
        try:
            tree = etree.parse(input_file)
        except etree.XMLSyntaxError:
            logging.error("XML syntaxerror in file " + input_file)
            if self.force:
                return
            else:
                sys.exit(-1)
        root = tree.getroot()
        for element in root.iter("gui_element"):           
            try:
                id = ''
                text = ''
                for prop in element:
                    if prop.tag == "id":
                        id = prop.text
                    if prop.tag == "text":
                        text = prop.text
                self.texts.append((id, text))                   
            except KeyError:
                pass

    def translate_mockups_in_directory(self, input_path):
        for infile in glob.glob(os.path.join(input_path, '*.bmml')):
                self.translate_mockup(infile)
        for infile in glob.glob(os.path.join(input_path + "/assets", '*.bmml')):
                self.translate_mockup(infile)

    def translate_mockup(self, input_file):
        pass



if __name__ == "__main__":

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-i', '--input', help='input-file or directory that will be read. When directory is given, all mockup-files in directory will be read.')
    PARSER.add_argument('-v', '--version', help='show version number.', action='store_true')
    PARSER.add_argument('--verbose', help='increase output verbosity.', action='store_true')
    ARGUMENTS = PARSER.parse_args()
    if ARGUMENTS.version:
        pass #TODO
        sys.exit(0)
    if not ARGUMENTS.input:
        logging.error('TODO')
        sys.exit(-1)
    if ARGUMENTS.verbose:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    mt = MockupTranslator(input_translation=ARGUMENTS.input)
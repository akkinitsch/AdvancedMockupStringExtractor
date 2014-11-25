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

class AdvancedMockupStringExtractor():
    """Class handling the extracting-process of text from Mockup-files."""

    controlElementsWithText = ["com.balsamiq.mockups::Label", "com.balsamiq.mockups::Paragraph", "com.balsamiq.mockups::TextArea", "com.balsamiq.mockups::TextInput", "com.balsamiq.mockups::SubTitle", "com.balsamiq.mockups::Button", "com.balsamiq.mockups::RadioButton", "com.balsamiq.mockups::Accordion", "com.balsamiq.mockups::Tooltip", "com.balsamiq.mockups::IconLabel", "com.balsamiq.mockups::ComboBox", "com.balsamiq.mockups::ButtonBar", "com.balsamiq.mockups::CheckBox", "com.balsamiq.mockups::Link"]
    # pylint: disable-msg=W0105
    """List of names of mockup-elements containing text."""

    texts = []
    """List with all recognized text in balsamiq-objects."""
    
    ignored = []
    """List with ignored texts in balsamiq-objects."""

    IgnoreTags = ["IGNORE", "IGNOREEXCLUDE"]
    """Tag indicating that element in balsamiq-file should be ignored."""

    listItemPattern = re.compile('\*%20[a-zA-z0-9 ]*(%0A){0,1}')
    """Pattern of regular expression that will be used to determine if a text containes list-items."""


    def __init__(self, input_file_dir=None, fake=None, force=False):
        """ Constructor.
            If input_file is given, only this file will be parsed. Otherwise all bmml-files in directory and subdirectories
            will be parsed.

            @param input_file_dir: file or directory that should be parsed (default None)
        """
        self.faketranslation = fake
        self.force = force
        if input_file_dir:
            if os.path.isfile(input_file_dir):
                self.extract_text(input_file_dir)
            else:
                self.extract_text_from_directory(input_file_dir)
        else:
            self.extract_text_from_directory(".")


    def extract_text(self, input_file):
        """ Extract text from mockup-elements by calling corresponding method for each mockup-element-type.

            Keyword arguments:
            @param input_file: mockup-file that should be parsed for texts.
        """
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
        for element in root.iter():
            try:
                self.extract_element_info(element, input_file)
            except KeyError:
                pass

    def extract_text_from_directory(self, input_path):
        logging.debug("In extract_text_from_directory")
        for infile in glob.glob(os.path.join(input_path, '*.bmml')):
                self.extract_text(infile)
        for infile in glob.glob(os.path.join(input_path + "/assets", '*.bmml')):
                self.extract_text(infile)

    def get_control_property(self, control_properties, tag):
        """ Return the text contained in an element-property with tag-element tag.

            Keyword arguments:
            @param control_properties: properties of an element.
            @param tag: tag of the property that should be returned.
        """
        for control_prop in control_properties:
            if control_prop.tag == tag:
                return control_prop.text
        return None #control-property not contained in properties of control

    def get_control_id(self, control_properties, input_file):
        """ Return the control-id of an element.

            Keyword arguments:
            @param control_properties: properties of an element
            @param input_file: input-file containing the element
        """
        result = self.get_control_property(control_properties, 'customID')
        if not result:
            #logging.error("\tElement without custom id in file %s\n\tText in element: %s", input_file, self.get_text(control_properties))
            #sys.exit(-1) #TODO hier weitermachen
            return False
        return result

    def get_text(self, control_properties):
        """ Return the text contained in an element.

            Keyword arguments:
            @param control_properties: properties of an element.
        """
        result = self.substitute_formatingchars(self.get_control_property(control_properties, 'text'))
        return TextFormatFixer.fix_text(result)

    def get_metainformation(self, control_properties):
        """ Return the metainformation contained in an element.

            Keyword arguments:
            @param control_properties: properties of an element.
        """
        return self.substitute_formatingchars(self.get_control_property(control_properties, 'customData'))

    def element_should_be_ignored(self, control_id):
        """ Return if an element and its text should be irgnored.

            Keyword arguments:
            @param control_id: control-id of an element.
        """
        if control_id.upper() in self.IgnoreTags:
            return True
        else:
            return False

    def checkElementWithoutText(self, element, input_file):
        """ Check if an element that does not have text that should be translated has got an id.
            For example this can happen if the user gives the id to a group of elements containing the
            element with text instead of giving the id to the element with text.

            If there is an element that has an id but should have no text, the program is aborted with a warning
            if the force-flag is not set to true.
        """
        for prop in element:
            id = self.get_control_id(prop, input_file)
            if id and not self.element_should_be_ignored(id):
                logging.warning("Element with ID should have no text\n\tID: %s\n\tcontrolType: %s\n\tfile: %s\n", id, element.attrib["controlTypeID"], input_file)
                if not self.force:
                    sys.exit(-1)

    def extract_element_info(self, element, input_file):
        """ Extract text from default mockup-elements (text, button etc.)
            Give error-message if there is already an element with same ID but different text.
            Appends all text-information as instance of class TextElement to list.

            @param element: xml-element from mockup-file.
            @param input_file: name of input-file.
        """
        if element.attrib["controlTypeID"] not in self.controlElementsWithText:
            self.checkElementWithoutText(element, input_file)
            return
        if element.attrib["controlTypeID"] == "com.balsamiq.mockups::ButtonBar":
            return self.extract_text_from_buttonbar(element, input_file)
        elif element.attrib["controlTypeID"] == "com.balsamiq.mockups::ComboBox":
            return self.extract_text_from_combobox(element, input_file)
        for control_properties in element:
            control_id = self.get_control_id(control_properties, input_file)
            text = self.get_text(control_properties)
            if self.get_control_property(control_properties, 'customData'):
                metainfo = self.substitute_formatingchars(self.get_control_property(control_properties, 'customData'))
            else:
                metainfo = None
            try:
                if self.faketranslation:
                    new_text_element = TextElement(control_id, '#'+ self.faketranslation + '# ' + text + ' #' + self.faketranslation + '#', input_file, metainfo)
                else:
                    new_text_element = TextElement(control_id, text, input_file, metainfo)
                if not self.element_should_be_ignored(control_id):
                    self.checkElementIdUnique(new_text_element)
                    if new_text_element in self.texts:
                        pass
                    else:
                        self.texts.append(new_text_element)
                else:
                    self.ignored.append(new_text_element)
            except AttributeError:
                pass

    def checkElementIdUnique(self, newElement):
        """ Check if an element with same ID was already extracted. If so, check if texts of both elements are the same.
            If the texts are not the same, exit program with an error-message.
        """
        for oldElement in self.texts:
            if oldElement.identifier == newElement.identifier and oldElement.text != newElement.text:
                logging.error("Element has got same ID but different text like other element: \n\tID: %s\n\ttext: %s\n\tfilename: %s\n\n\tID: %s\n\ttext: %s\n\tfilename: %s", newElement.identifier, newElement.text, newElement.filename, oldElement.identifier, oldElement.text, oldElement.filename)
                if not self.force:
                    sys.exit(-1)

    def get_text_from_combined_element(self, element, input_file, seperator):
        """ Extracts texts from element holding more than one text. TextElements will return an index to make sure that
            the order of the texts can be comprehended.

            Keyword arguments:
            @param element: xml-element from mockup-file.
            @param input_file: input-file containing the element.
            @parameter seperator: seperator that is used to divide different texts in the text-property.
        """
        for control_properties in element:
            control_id = self.get_control_id(control_properties, input_file)
            texts = self.get_text(control_properties).split(seperator)
            if self.get_control_property(control_properties, 'customData'):
                metainfo = self.substitute_formatingchars(self.get_control_property(control_properties, 'customData'))
            else:
                metainfo = None
            index = 0
            for text in texts:
                try:
                    if not self.element_should_be_ignored(control_id):
                        self.texts.append(TextElement(control_id + "_" + text.replace(' ', ''), text, input_file, metainfo, index))
                        index = index + 1
                except AttributeError:
                    pass


    def extract_text_from_buttonbar(self, element, input_file):
        """Extracts texts from buttonbar-elements and append them to self.texts.
        The appended elements will have an index to be able to distinguish the elements of the buttonbar and to
        know the order they are contained in the buttonbar.
        """
        self.get_text_from_combined_element(element, input_file, '%2C')

    def extract_text_from_combobox(self, element, input_file):
        """Extracts texts from combobox-elements and append them to self.texts.
        The appended elements will have an index to be able to distinguish the elements of the combobox and to
        know the order they are contained in the combobox.
        """
        self.get_text_from_combined_element(element, input_file, '<br />')

    def containes_unordered_list(self, text):
        """Returns True if the text containes an unordered list, otherwise returns False"""
        return self.listItemPattern.match(text)

    def substitute_unordered_list(self, text):
        """Replaces the markdown-markup of an unordered list with html-markup of an unordered list."""
        if not self.containes_unordered_list(text):
            return text
        else:
            items = re.split('\*%20', text)
            result = '<ul>'
            for item in items:
                if item:#item not empty
                    result = result + '<li>' + item + '</li>'
            result = result + '</ul>'
            return result

    def substitute_formatingchars(self, text):
        """ Remove all formating chars from mockup.

            @param text: Text element from mockup containing format-information.
            @return: Tuple containing text and format-information.
        """
        result = ""
        try:
            result = text.replace("%0A", "<br />") #prevend newlines from beeing unquoted
            result = self.remove_multiple_whitespaces(result)
            result = result.replace("breakNewLine", ' <br />')
            result = result.replace("<br /> ", "<br />")
            result = result.replace(" <br />", "<br />")
            result = result.replace(" <li>", "<li>") 
            result = result.replace("<li> ", "<li>") 
            result = self.substitute_bold(result)
        except AttributeError:
            logging.debug("Trying to substitute formating and html-chars in empty string.")
        return result

    def substitute_bold(self, text):
        """Return text where markdown-markup for bold text (with two asterixes) is replaced with html-markup for bold text."""
        return re.sub(r'\*(.*?)\*', r'<b>\1</b>', text)

    def substitute_italic(self, text):
        """Return text where markdown-markup for italic text (with two underscores) is replaced with html-markup for italic text."""
        return re.sub(r'_(.*?)_', r'<i>\1</i>', text)

    def remove_multiple_whitespaces(self, text):
        """Return text where multiple whitespaces are replaced with only one whitespace."""
        return re.sub( '\s+', ' ', text).strip()

    def check_ignored_texts(self):
        """Check that the text of every text-element that is set to be ignored is included in another not ignored text-element."""
        for ignored in self.ignored:
            contained = False
            for text in self.texts:
                if text.text == ignored.text:
                    contained = True
            if contained:
                continue
            else:
                logging.error("Ignored text not in self.texts: %s %s ", ignored.filename,  ignored.text)

if __name__ == "__main__":

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-c', '--check', help='do not generate output, just check if all ids of textelements are given.', action='store_true')
    PARSER.add_argument('--faketranslation', help='generate fake translation-output. Will add given parameter as prefix and postfix to every text in output-file')
    PARSER.add_argument('-f', '--force', help='force generating outpu-file even if errors occure.', action='store_true')
    PARSER.add_argument('-i', '--input', help='input-file or directory that will be read. When directory is given, all mockup-files in directory will be read.')
    PARSER.add_argument('--json', help='write output in json-format instead of xml-format.', action='store_true')
    PARSER.add_argument('-min', '--minified', help='remove whitespaces from generated output.', action='store_true')
    PARSER.add_argument('-o', '--output', help='name of file that will contain the generated output.')
    PARSER.add_argument('-v', '--version', help='show version number.', action='store_true')
    PARSER.add_argument('--verbose', help='increase output verbosity.', action='store_true')

    ARGUMENTS = PARSER.parse_args()
    if ARGUMENTS.version:
        print 'AdvancedMockupStringExtractor V', __version__
        sys.exit(0)
    if not ARGUMENTS.output and not ARGUMENTS.check:
        logging.error('You have to give the name of the output-file there the generated data will be stored in.')
        sys.exit(-1)
    if ARGUMENTS.verbose:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    if ARGUMENTS.force:
        force = True
    if ARGUMENTS.input:
        EXTRACTOR = AdvancedMockupStringExtractor(ARGUMENTS.input, fake=ARGUMENTS.faketranslation, force=ARGUMENTS.force)
    else:
        EXTRACTOR = AdvancedMockupStringExtractor(fake=ARGUMENTS.faketranslation, force=ARGUMENTS.force)
    if ARGUMENTS.faketranslation:
        EXTRACTOR.faketranslation = ARGUMENTS.faketranslation
    if ARGUMENTS.check:
        EXTRACTOR.check_ignored_texts()
        sys.exit(0)
    EXPORTER = OutputExporter(EXTRACTOR.texts)
    if ARGUMENTS.json:
        EXPORTER.json_export(ARGUMENTS.output, ARGUMENTS.minified)
    else:
        EXPORTER.xml_export(ARGUMENTS.output, ARGUMENTS.minified)
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


"""This module containes a class that is used to write extractedtexts from balsamiq-mockup-files into files.
"""

import logging
import urllib

from lxml import etree

class OutputExporter:
    """ Class that manages writing the results from MockupStringExtractors to output-files in JSON or XML-format.
    """

    def __init__(self, texts, encoding='ISO-8859-1'):
        """ Get texts that should be exported at init-time"""
        self.texts = texts
        self.output_encoding = encoding

    def unescape_html(self, text):
        """ Unescape HTML-encoding and special characters from html-formated text in mockups.

            @param text: input text.
            @return: text with html-letters and special characters replaced.
        """
        result = urllib.unquote_plus(urllib.unquote_plus(text.encode('utf8')))
        result = result.replace("&#196;", "Ä")
        result = result.replace("&#214;", "Ö")
        result = result.replace("&#220;", "Ü")
        result = result.replace("&#223;", "ß")
        result = result.replace("&#228;", "ä")
        result = result.replace("&#246;", "ö")
        result = result.replace("&#252;", "ü")
        result = result.replace("&amp;", "&")
        result = result.replace("&lt;", "<")
        result = result.replace("&gt;", ">")
        return result


    def string_to_json_value(self, text):
        """Makes string compatible so it can be used as json-value."""
        return text.replace('\"', '\\\"')

    def json_export(self, output_file, minified=False):
        """ Write all texts to file in JSON-format.

            @param output_file: path and name outputfile output-file.
            @param minified: Flag indicating if whitespaces should be removed from output (default False).
        """
        logging.info("Writing JSON-export to file " + output_file)
        outputfile = open(output_file, "w")
        outputfile.write("{")
        if not minified:
            outputfile.write("\n")
            self.texts.sort()
            for text in self.texts[:-1]:
                outputfile.write('\t\"%s\":\"%s\",\n' %(text.identifier, self.string_to_json_value(text.text)))
            try:
                outputfile.write('\t\"%s\":\"%s\"\n' %(self.texts[-1].identifier, self.string_to_json_value(self.texts[-1].text)))
            except IndexError:
                pass #no texts in self.texts
        else:
            for text in self.texts[:-1]:
                try:
                    outputfile.write('\"%s\":\"%s\",' %(text.identifier, self.string_to_json_value(text.text)))
                except AttributeError:
                    logging.error(text.text)
                except IndexError:
                    pass #no texts in self.texts
            try:
                outputfile.write('\"%s\":\"%s\"' %(self.texts[-1].identifier, self.string_to_json_value(self.texts[-1].text)))
            except AttributeError:
                logging.error("Error in last element: %s", self.string_to_json_value(text.text))
            except IndexError:
                pass #no texts in self.texts
        outputfile.write("}")
        outputfile.close()

    def xml_export(self, output_file, minified=False):
        """ Write all texts to file in XML-format.

            @param output_file: path and name outputfile output-file.
            @param minified: Flag indicating if whitespaces should be removed from output (default False).
        """
        root = etree.Element("root")
        self.texts.sort()
        for txt in self.texts:
            child = etree.SubElement(root, "gui_element")
            text_element = etree.SubElement(child, "file")
            text_element.text = txt.filename
            id_element = etree.SubElement(child, "id")
            id_element.text = txt.identifier.decode('unicode-escape')
            id_element.text = id_element.text.replace(" ", "_")
            index_element = etree.SubElement(child, "index")
            index_element.text = str(txt.index)
            text_element = etree.SubElement(child, "text")
            try:
                text_element.text = txt.text.decode('unicode-escape')
            except ValueError:
                logging.error("Value-error in text-element %s", txt.text)
            text_element = etree.SubElement(child, "metainformation")
            try:
                text_element.text = txt.meta.decode('unicode-escape')
            except AttributeError: #None-Type object -> no meta-information in mockup
                pass
        logging.info("Writing XML-export to file " + output_file)
        outputfile = open(output_file, "w")
        if minified:
            outputfile.write(self.unescape_html(etree.tostring(root, pretty_print=False, xml_declaration=True, encoding=self.output_encoding).encode('utf8')))
        else:
            outputfile.write(self.unescape_html(etree.tostring(root, pretty_print=True, xml_declaration=True, encoding=self.output_encoding).encode('utf8')))
        outputfile.close()

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
import shutil
import sys

from lxml import etree

from AdvancedMockupStringExtractor import ControlElementsWithText

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class MockupTranslator():
	
	def __init__(self, mockupSourceDirectory, translationFile):
		self.srcDir = mockupSourceDirectory
		self.targetDir = "./test"
		self.translationFile = translationFile
		self.translationTree = etree.parse(self.translationFile)
		self.translationRoot = self.translationTree.getroot()

	def textWithCustomIDinControl(self, control):
		for control_properties in control:
			for control_property in control_properties:
				if control_property.tag == 'customID' and control_property.text != "ignore":
					return True
		return False

	def getCustomID(self, prop):
		if prop.tag == 'customID' and prop.text != "ignore":
			return prop.text

	def findTranslation(self, customId):
		for guiElement in self.translationRoot:
			for element_entry in guiElement:
				if element_entry.tag == 'id' and element_entry.text == customId:
					for element_entry2 in guiElement:
						if element_entry2.tag == 'text':
							return element_entry2.text
		return "foobar"


	def translateMockup(self, file):
		translation = ""
		fileTree = etree.parse(file)
		fileRoot = fileTree.getroot()
		for controls in fileRoot:
			for control in controls:
				if control.attrib['controlTypeID'] in ControlElementsWithText:
					for control_properties in control:
						for control_property in control_properties:
							cId = self.getCustomID(control_property)
							if cId:
								t = self.findTranslation(cId)
								for control_property2 in control_properties:
									if control_property2.tag == "text":
										control_property2.text = t
		fileTree.write(file)
            #self.extract_element_info(element, input_file)

	def translateMockups(self, outputDir='./translation'):
		shutil.copytree(self.srcDir, outputDir)
		for inFile in glob.glob(os.path.join(outputDir, '*.bmml')):
		#for infile in glob.glob(os.path.join(self.srcDir, '*.bmml')):
			self.translateMockup(inFile)

if __name__ == "__main__":
	mt = MockupTranslator("/home/akki/tmp/Mockupstuff/mockups_Hai/Wireframes/", "/home/akki/tmp/Mockupstuff/wombatTool/input/webui_hai_mockups_2014-10-14_EN.xml")
	mt.translateMockups()
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


"""These are unittests for module AdvancedMockupStringExtractor."""

import unittest
import logging

import AdvancedMockupStringExtractor

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)

class AdvancedMockupStringExtractorTest(unittest.TestCase):
    """Class that represents the testcases."""

    # pylint: disable-msg=C0103
    def setUp(self): # pyunit makes this name needed.
        self.extractor = AdvancedMockupStringExtractor.AdvancedMockupStringExtractor()

    def testSubstituteBoldWithTwoStars(self):
        """Test if bold text marked with two stars will be marked with bold-tags."""
        result = self.extractor.substitute_bold('*bold*')
        self.assertEqual(result, '<b>bold</b>')

    def testSubstituteItalicWithTwoUnderscores(self):
        """Test if italic text marked with two underscores will be marked with italic-tags."""
        result = self.extractor.substitute_italic('_italic_')
        self.assertEqual(result, '<i>italic</i>')

    def testDetectUnorderedListInTextPositive(self):
        """Test if the detection of an unordered list in text is successful."""
        inputString = '*%20item1%0A*%20item2%0A*%20item3'
        self.assertTrue(self.extractor.containes_unordered_list(inputString))

    def testDetectUnorderedListInTextNegative(self):
        """"Test if the detection of an unordered list in text without asterics failes."""
        inputString = 'this is a text'
        self.assertFalse(self.extractor.containes_unordered_list(inputString))

    def testDetectUnorderedListInTextNegative2(self):
        """"Test if the detection of an unordered list in text with bold texts only failes."""
        inputString = '*bold1* *bold2* bold3*'
        self.assertFalse(self.extractor.containes_unordered_list(inputString))


    def testSubstituteListItemsWithStars(self):
        """Test if listitems marked with stars will be marked with listitem-tags."""
        inputString = '*%20item1%0A*%20item2%0A*%20item3'
        result = self.extractor.substitute_unordered_list(inputString)
        wantedResult = '<ul><li>item1%0A</li><li>item2%0A</li><li>item3</li></ul>'
        self.assertEqual(result, wantedResult)

    @unittest.skip("This is a todo for a later version.")
    def testSubstituteListItemsWithStarsAndPrecededText(self):
        """Test if listitems marked with stars and with preceding text will be marked with listitem-tags."""
        inputString = 'Text before*%20item1%0A*%20item2%0A*%20item3'
        result = self.extractor.substituteUnorderedList(inputString)
        wantedResult = 'Text before%0A<ul><li>item1</li><li>item2</li><li>item3</li></ul>'
        self.assertEqual(result, wantedResult)

    @unittest.skip("This is a todo for a later version.")
    def testExtractRadioButtonText(self):
        self.extractor.extract_text('./test_input/RadioButton01.bmml')
        extractedText = None
        for textElement in self.extractor.texts:
            if textElement.identifier == "firstElement":
                extractedText = textElement.text
        self.assertEqual(extractedText, 'Text in RadioButton')


if __name__ == '__main__':
    TESTSUITE = unittest.TestLoader().loadTestsFromTestCase(AdvancedMockupStringExtractorTest)
    unittest.TextTestRunner(verbosity=1).run(TESTSUITE)


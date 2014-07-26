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


import unittest

from TextFormatFixer import TextFormatFixer

class TextFormatFixerTest(unittest.TestCase):
    """Unittests for class TextformatFixer."""

    def test_remove_leading_spaces(self):
        """Test if leading spaces are removed from a text."""
        result = TextFormatFixer.fix_text('   Text with leading spaces.')
        self.assertEqual(result, 'Text with leading spaces.')

    def test_remove_trailing_spaces(self):
        """Test if leading spaces are removed from a text."""
        result = TextFormatFixer.fix_text('Text with leading spaces.   ')
        self.assertEqual(result, 'Text with leading spaces.')

    def test_replace_html_whitespaces(self):
        """Test if html-whitespaces are replaced correctly"""
        result = TextFormatFixer.fix_text('Text%20with%20html%20whitespaces.')
        self.assertEqual(result, 'Text with html whitespaces.')

    def test_remove_spaces_after_br(self):
        """Test if leading spaces after a html-linebreak are removed"""
        result = TextFormatFixer.fix_text('this is a text<br />     containing a linebreak')
        self.assertEqual(result, 'this is a text<br />containing a linebreak')

if __name__ == '__main__':
    TESTSUITE = unittest.TestLoader().loadTestsFromTestCase(TextFormatFixerTest)
    unittest.TextTestRunner(verbosity=1).run(TESTSUITE)

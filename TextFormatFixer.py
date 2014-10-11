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

import re

class TextFormatFixer():
    """Class that fixes format from balsamiq-mockups to plain text."""

    def __init__(self):
        pass

    @staticmethod
    def fix_text(text):
        """Wrapper that uses all static methods of this class on an text.

            Keyword arguments:
            @param text: Text containing fext-formats that are not wanted for use in software and that should be corrected.
        """
        result = TextFormatFixer.replace_html_whitespaces(text)
        result = TextFormatFixer.remove_leading_trailing_spaces(result)
        result = TextFormatFixer.remove_spaces_after_br(result)
        return result

    @staticmethod
    def remove_leading_trailing_spaces(text):
        """Removes leading and trailing whitespaces from input-string

            Keyword arguments:
            @param text: Text that should be corrected.
        """
        try:
            return text.strip()
        except:
            return ''

    @staticmethod
    def replace_html_whitespaces(text):
        """Replacing spaces in html-syntax with spaces.

            Keyword arguments:
            @param text: Text that should be corrected.
        """
        try:
            return text.replace('%20', ' ')
        except:
            return ''

    @staticmethod
    def remove_spaces_after_br(text):
        """Remove leading whitespaces after an br-tag.

            Keyword arguments:
            @param text: Text that should be corrected.
        """
        try:
            return re.sub(r'<br />[ ]*', '<br />', text)
        except:
            return ''

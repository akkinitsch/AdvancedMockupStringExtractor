#AdvancedMockupStringExtractor

Script for extracting texts from mockups created with Balsamiq Mockups

#Purpose

The purpose of this script is to extract text-elements in an XML-format
usable as input of an translation memory system (TMS).

After the mockups were finished and approved by all parties involved in
the specification-process of the software, implementation of the software
and translation of the GUI can start at the same time.
When changes of texts are neccessary, they can be done first in the mockups
and they will be regarded in the next translation-cycle without the need to
wait for the next software-version cycle.
This should give the translators more time for their part and should result
in better translations.

The first project i used the script in used JSON-files as input-format of
texts. I implemented a JSON-export, so i was able to use the texts from the
mockups during implementation (of course in source language only).

#Requirements
* python 2.7.x
* lxml version 2.3.2 or above

#How to use

##Preperating the mockups

###Identifier of mockup-elements

Via the context menu of each element in Balsamiq Mockups you can edit the
*Custom Control Propertie* of each element in a mockup. The property
*Custom control ID* will be used as an identifier for each element.

Every element needs to have an unique name in this property. If you want
to extract the elements of different mockup-files into one output-file, you
have to mark the second and all following appearances of the same element
with the Custom control ID "ignore".

If you have to change the content of an element that appears more than
once in all mockups, make sure to change all (or at least the first) appearance
of this element.

###(Meta-)Information for translators
Via the context menu of each element in Balsamiq Mockups you can edit the
*Custom Data Property* of each element in a mockup. The property
*Custom Data* will be used for generating metainformation for the translator in
the exported XML-file. Use this field to give additional information to the
translator that can be useful for his work.

##Extracting texts from mockups

###Checking if mockups are prepared well
Before extracting texts from the mockups, you can check if the mockups are prepared
well. The program will show you

* elements that do not have any identifier.
* elements with same identifier but different texts.
* elements that are ignored without an element with same text that are not ignored.

Check your mockups doing this:

    python AdvancedMockupStringExtractor.py --check

###Extracting texts from all mockups in a directory 

To extract the texts in all mockups in a directory, start the AdvancedMockupStringExtractor
within that directory and specify the name of the output file:

    python AdvancedMockupStringExtractor.py -o outputfile.xml

As default, the program will extract all textes and their metadata into a
XML file.

###Extracting text from only one mockup-file
You can extract the text from only one mockup-file by specifiing an input file:

    python AdvancedMockupStringExtractor.py -o outputfile.xml -i inputfile.bmml

###Exporting texts to json-file instead of an xml-file

    python AdvancedMockupStringExtractor.py -o outputfile.json --json

### Exporting minified output
With these option, the program will remove unneccessary whitespaces from the generated output:

    python AdvancedMockupStringExtractor.py -o outputfile.xml --min

#TODOs
* Adding option to search for mockup-files in directories recursively.
* Choosing output-format depending on file-extension of output-file.
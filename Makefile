build:
	make pylint
	make codeanalysis
	make unittests
	make check_documentation
	make clean

tests:
	python AdvancedMockupStringExtractorTest.py

codeanalysis:
	radon cc -anc AdvancedMockupStringExtractor.py
	radon mi AdvancedMockupStringExtractor.py

check_documentation:
	epydoc --check -v AdvancedMockupStringExtractor.py

doc:
	#epydoc --pdf -o documentation AdvancedMockupStringExtractor.py
	epydoc --html -o documentation AdvancedMockupStringExtractor.py

pylint:
	pylint AdvancedMockupStringExtractor.py

still:
	python AdvancedMockupStringExtractor.py --o test2.xml
	diff test.xml test2.xml

clean:
	rm -rf *.pyc
	rm -rf documentation
	rm -rf test*
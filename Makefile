.PHONY: clean
clean:
		@rm -f example.sqlite
		@rm -Rf dist/
		@rm -Rf build/
		@rm -Rf indexes/
		@rm -Rf __pycache__/
		@rm -Rf ponyindexes/
		@rm -Rf ponywhoosh.egg-info
		@find . -name "*.pyc" -type f -delete

# ========= Python 2.7 =============================================

.PHONY: install-py2
install-py2 :
		make clean
		python2 setup.py install


.PHONY: test-py2
test-py2:
		make install-py2
		python2 -m unittest test

# ========= Python 3 ===============================================

.PHONY: install-py3
install-py3 :
		make clean
		python3 setup.py install

.PHONY: test-py3
test-py3 :
		make install-py3
		python3 -m unittest test

.PHONY : default
default :
		test-py2
		make clean
		test-py3


.PHONY: pip-package
pip-package:
	rm -Rf dist
	rm -Rf build
	python setup.py build
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

# pip install twine

.PHONY : deploy 
deploy : 
	$(eval VERSION := $(shell bash -c 'read -p "Version: " pwd; echo $$pwd'))
	echo
	$(eval MSG := $(shell bash -c 'read -p "Comment: " pwd; echo $$pwd'))
	git add .
	git tag v$(VERSION)
	git commit -am "[ v$(VERSION) ] new version: $(MSG)"
	make pip-package
	git push origin master --tags
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

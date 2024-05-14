.PHONY: clean clean-test clean-pyc clean-build
.DEFAULT_GOAL := test

clean: clean-build clean-pyc clean-test  ## remove all build, test, coverage and Python artifacts

clean-build:  ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:  ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:  ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint:  ## check style with flake8
	flake8 sopel-trakt tests

test:  ## run tests quickly with the default Python
	python -m pytest

coverage:  ## check code coverage quickly with the default Python
	coverage run --source sopel_modules/trakt -m pytest
	coverage report -m

install: clean ## install the package to the active Python's site-packages
	python setup.py install

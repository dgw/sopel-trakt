.PHONY: clean clean-test clean-pyc clean-build
.DEFAULT_GOAL := test

clean-all: clean clean-pyc clean-test  ## remove all build, test, coverage and Python artifacts

clean:  ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:  ## remove Python file cache artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:  ## remove test and coverage artifacts
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

lint:  ## check style with flake8
	flake8 sopel_trakt tests

test:  ## run tests quickly with the default Python
	python -m pytest

coverage:  ## check code coverage quickly with the default Python
	coverage run --source sopel_trakt -m pytest
	coverage report -m

install:  ## install the package to the active Python's site-packages
	python -m pip install .

dev:  ## install for development
	python -m pip install -e . -r dev-requirements.txt

undev:  ## uninstall development package (does not remove dev dependencies)
	python -m pip uninstall -y sopel-trakt
	rm -fr sopel_trakt.egg-info/

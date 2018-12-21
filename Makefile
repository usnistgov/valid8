.PHONY: help test coverage clean
.DEFAULT: help

help:
	@echo "make test"
	@echo "       run tests with coverage"
	@echo "make coverage"
	@echo "       show coverage reports"

TEST_COMMAND=pytest -s test/ -v
SRC_DIR=./rbv

dep:
	pip install -q -r requirements.txt

build: dep
	python setup.py install

devdep:
	pip install -q pytest coverage

test: dep devdep
	$(TEST_COMMAND)

coverage: dep devdep
	coverage run --branch --source=$(SRC_DIR) -m $(TEST_COMMAND)
	coverage report -m
	coverage html

clean:
	rm -rf dist *.egg-info build doc/api htmlcov .pytest_cache .coverage

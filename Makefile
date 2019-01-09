.PHONY: help dep build devdep test coverage quality clean
.DEFAULT: help

help:
	@echo "make test"
	@echo "       run tests with coverage"
	@echo "make coverage"
	@echo "       show coverage reports"
	@echo "make build"
	@echo "       install package"
	@echo "make quality"
	@echo "       run quality checks"
	@echo "make clean"
	@echo "       delete all intermediary files"

TEST_COMMAND=pytest -s test/ -v
SRC_DIR=./rbv
CLEAN_TARGETS=dist *.egg-info build doc/api htmlcov .pytest_cache .coverage

dep:
	pip install -q -r requirements.txt

build: dep
	python setup.py install

devdep:
	pip install -q pytest>=3.9 coverage

test: dep devdep
	$(TEST_COMMAND)

coverage: dep devdep
	coverage run --branch --source=$(SRC_DIR) -m $(TEST_COMMAND)
	coverage report -m
	coverage html

quality:
	pip install -q flake8
	flake8 --ignore=E501,F401

clean:
	rm -rf $(CLEAN_TARGETS)

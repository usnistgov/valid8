.PHONY: help dep build devbuild devdep test coverage quality clean format
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

build:
	python setup.py install

devbuild:
	pip install -e .

devdep:
	pip install -q 'pytest>=3.9' coverage black flake8

test:
	$(TEST_COMMAND)

coverage:
	coverage run --branch --source=$(SRC_DIR) -m $(TEST_COMMAND)
	coverage report -m
	coverage html

quality:
	flake8 --ignore=E501,F401

clean:
	rm -rf $(CLEAN_TARGETS)

format:
	python -m black .

.PHONY: help dep build devbuild devdep test coverage quality clean
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

devbuild: devdep
	pip install -e .

devdep: dep
	pip install -q 'pytest>=3.9' coverage black flake8 pre-commit
	pre-commit install

test:
	$(TEST_COMMAND)

coverage:
	coverage run --branch --source=$(SRC_DIR) -m $(TEST_COMMAND)
	coverage report -m
	coverage html

quality:
	python -m black .
	flake8  # options are in setup.cfg

clean:
	rm -rf $(CLEAN_TARGETS)


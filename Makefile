.PHONY: help dep install devinstall devdep clean
.DEFAULT: help

help:
	@echo "make devinstall"
	@echo "       sets up the local dev environment"
	@echo "make clean"
	@echo "       delete all intermediary files"

DOC_TARGETS=doc/**/api doc/_build
CLEAN_TARGETS=dist *.egg-info build htmlcov .pytest_cache .coverage .tox $(DOC_TARGETS)

dep:
	pip install -q -r requirements.txt

install: dep
	python setup.py install

devinstall: devdep
	pip install -e .

devdep: dep
	pip install -q 'pytest>=3.9' coverage black flake8 pre-commit tox
	pre-commit install

clean:
	rm -rf $(CLEAN_TARGETS)

docs_clean:
	rm -rf $(DOC_TARGETS)

publish_to_github:
	bash -x publish_to_github.sh

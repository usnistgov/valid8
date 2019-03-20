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

publish_to_gitlab: 
	git remote rm github || echo "github remote does not need to be deleted"
	git remote add github $GITHUB_MIRROR && git fetch -v --all
	git push github master:master
	git clone --single-branch -b nist-pages $GITHUB_MIRROR nist_pages
	cd nist_pages
	git ls-files | xargs rm -f
	cp -r ../html_docs/* .
	git config --global user.email "datascience@nist.gov"
	git config --global user.name "NIST MIG datascience bot"
	touch .nojekyll
	git add . .nojekyll
	git commit -am "Automatic update for nist_pages."
	git push origin nist-pages

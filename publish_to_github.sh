#!/usr/bin/env bash

GITHUB_MIRROR=https://$GITHUB_USERNAME:$GITHUB_TOKEN@github.com/usnistgov/valid8.git

git remote rm github || echo "github remote does not need to be deleted"
git remote add github $GITHUB_MIRROR && git fetch -v --all
git checkout -f master && git push github master:master
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

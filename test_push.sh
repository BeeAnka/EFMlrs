#!/bin/bash
if [ -z "$1" ] || [ -z "$2" ]
then
  print usage: $0 "[version] [commit]"
  exit 1
fi
rm dist/*
git commit -m "$2"
git push
git tag -a "$1" -m "$2"
python ./setup.py sdist
python ./setup.py bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

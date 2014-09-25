all: pylint test-all

pylint:
	find . -maxdepth 1 -type d | grep -v ".git" | xargs flake8
test-all:
	find . -maxdepth 1 -type d | grep -v ".git" | xargs nosetests -w

.PHONY: pylint test-all

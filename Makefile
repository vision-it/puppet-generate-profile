.PHONY: test lint coverage

test:
	py.test
coverage:
	py.test --cov-report term-missing -v --cov profile-generate
lint:
	pylint profile-generate.py

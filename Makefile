.PHONY: env
env:
	conda create -q -n jedi python=3.7 pip

.PHONY: format
format:
	isort -rc --atomic jedi/
	black --line-length 79 jedi/

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: test
test:
	nosetests jedi/

.PHONY: env
env:
	conda create -q -n flask_web_skeleton python=3.7 pip

.PHONY: format
format:
	isort -rc --atomic flask_web_skeleton/
	black --line-length 79 flask_web_skeleton/

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: test
test:
	nosetests flask_web_skeleton/

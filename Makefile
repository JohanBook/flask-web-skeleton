.PHONY: format
format:
	isort -rc --atomic flask_web_skeleton/
	black --line-length 79 flask_web_skeleton/

.PHONY: test
test:
	nosetests flask_web_skeleton/

.PHONY: env
env:
	conda create -q -n jedi python=3.7 pip

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: reset
reset:
	python -c "from flask_blog import db; db.drop_all(); db.create_all()"

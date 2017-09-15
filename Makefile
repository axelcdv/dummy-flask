.PHONY: test init

env:
	virtualenv -p python3 env

init: env
	env/bin/pip install -r requirements.txt

test:
	env/bin/nosetests

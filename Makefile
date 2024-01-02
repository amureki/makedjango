requirements:
	pip-compile --upgrade --rebuild requirements.in > /dev/null
	pip-compile --upgrade --rebuild requirements-test.in > /dev/null

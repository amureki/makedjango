requirements:
	pip-compile --upgrade --rebuild --no-annotate --no-header requirements.in > /dev/null
	pip-compile --upgrade --rebuild --no-annotate --no-header requirements_test.in > /dev/null

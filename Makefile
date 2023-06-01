.SILENT: fmt check lint bandit

fmt:
	find . -type d -name ".venv" -prune -o -print -type f -name "*.py" \
		-exec pyupgrade \
			--exit-zero-even-if-changed \
			--keep-runtime-typing \
			--py38-plus \
			{} \+ 1> /dev/null
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		src/flake8_flask_openapi_docstring tests
	isort --profile black .
	black .

bandit:
	bandit -q -r src/flake8_flask_openapi_docstring
	bandit -q -lll -r tests

check: bandit
	find . -type d -name ".venv" -prune -o -print -type f -name "*.py" \
		-exec pyupgrade \
			--keep-runtime-typing \
			--py38-plus \
			{} \+ 1> /dev/null
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		-c \
		src/flake8_flask_openapi_docstring tests
	isort --profile black -c .
	black --check .

lint: bandit
	mypy src/flake8_flask_openapi_docstring
	flake8 .

test:
	pytest -x --cov=core --cov=flake8_flask_openapi_docstring --cov-fail-under=90

install:
	poetry install --sync

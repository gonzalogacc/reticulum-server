
.PHONY: install
install:
	uv sync
	uv run pre-commit install

.PHONY: run
run:
	uv run python main.py

.PHONY: check
check:
	uv run ruff check

.PHONY: fix
fix:
	uv run ruff check --fix

.PHONY: mypy
mypy:
	uv run mypy *.py
PYTHON = python3
UV = uv

.PHONY: all install run debug clean lint format build

all: install lint run

install:
	$(UV) sync

run:
	$(UV) run pac-man.py config.json

debug:
	$(UV) run python -m pdb

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache dist/ build/
	find . -type d -name "__pycache__" -exec rm -r {} +

lint:
	uv run mypy . --exclude .venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	uv run flake8 . --exclude=.venv

build:
	$(UV) run pyinstaller pacman.spec --clean --noconfirm

format:
	ruff format .
	ruff check --fix .

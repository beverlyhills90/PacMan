PYTHON = python3
UV = uv

.PHONY: all install run debug clean lint format

all: install lint run

install:
	$(UV) sync

run:
	$(UV) run pac-man.py config.json

debug:
	$(PYTHON) -m pdb pac-man.py config.json

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -r {} +

test:
	$(UV) run pytest

lint:
	uv run mypy . --exclude .venv --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	uv run flake8 . --exclude=.venv

build:
	$(UV) run pyinstaller pacman.spec --clean --noconfirm

format:
	ruff format .
	ruff check --fix .

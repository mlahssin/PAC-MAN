.PHONY: install run debug clean lint

ARGS = config.json

install:
	uv sync

run:
	uv run python main.py $(ARGS)

debug:
	uv run python -m pdb main.py $(ARGS)

clean:
	find . -type d -name "__pycache__" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

lint:
	uv run flake8 .
	uv run mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs
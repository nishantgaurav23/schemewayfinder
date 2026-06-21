.PHONY: test lint eval mcp run deploy

test:
	uv run pytest tests/ -v --tb=short

lint:
	uv run ruff check app/ tests/
	uv run ruff format --check app/ tests/

eval:
	uv run python -m eval.scorer

mcp:
	uv run python -m app.mcp.scheme_search.server

run:
	uv run python -m app.main

deploy:
	bash deploy/deploy.sh

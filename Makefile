UV_CACHE_DIR ?= .uv-cache

.PHONY: test lint smoke pilot pilot-report

test:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --group dev pytest

lint:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run --group dev ruff check .

smoke:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run spinning-arrow smoke --spend-cap-usd 0.01 --max-call-cost-usd 0.01

pilot:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run spinning-arrow pilot --workers 4

pilot-report:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run spinning-arrow pilot-report $(RUN_ID)

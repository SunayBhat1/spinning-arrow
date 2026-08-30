UV_CACHE_DIR ?= .uv-cache

.PHONY: test lint smoke pilot pilot-report phase2 phase2-report

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

phase2:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run spinning-arrow phase2 --workers 12

phase2-report:
	UV_CACHE_DIR=$(UV_CACHE_DIR) uv run spinning-arrow phase2-report $(RUN_ID)

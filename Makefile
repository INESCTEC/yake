install:
	uv pip install --upgrade pip
	uv pip install -e .

install-dev:
	uv pip install --upgrade pip
	uv pip install -e ".[dev]"

test:
	uv run pytest -vv --cov=yake tests/ test_*.py

format:
	uv run black .

lint:
	uv run ruff check --fix .
	uv run ruff check .
	uv run flake8 yake/

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

build:
	uv build

deploy:
	uv build
	uv publish

all: install-dev lint test format

# Development benchmarks (código local)
benchmark-dev:
	python scripts/benchmark_dev.py

benchmark-dev-quick:
	PYTHONPATH=. python scripts/benchmark_dev.py

benchmark-compare-dev:
	python scripts/compare_benchmarks.py

# Benchmark oficial (código instalado)
benchmark:
	uv run pytest --benchmark-only tests/test_benchmark.py -v

benchmark-save:
	uv run pytest --benchmark-only --benchmark-save=baseline --benchmark-save-data tests/test_benchmark.py

benchmark-compare:
	uv run pytest --benchmark-only --benchmark-compare=baseline tests/test_benchmark.py

benchmark-report:
	uv run pytest --benchmark-only --benchmark-histogram=benchmark_histogram tests/test_benchmark.py

benchmark-install:
	uv add --optional benchmark pytest-benchmark memory-profiler matplotlib

benchmark-clean:
	rm -rf .benchmarks/ benchmark_histogram.svg
	rm -f benchmark_results_*.json

.PHONY: install install-dev test format lint clean build deploy all benchmark benchmark-save benchmark-compare benchmark-report benchmark-install benchmark-clean benchmark-dev benchmark-dev-quick benchmark-compare-dev
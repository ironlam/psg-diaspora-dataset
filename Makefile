.PHONY: setup test analyze charts collect retry-93-95 clean

# Setup development environment
setup:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

# Run tests
test:
	./venv/bin/pytest tests/ -v

# Run analysis
analyze:
	./venv/bin/python src/analysis/analyze_players.py

# Generate charts
charts:
	./venv/bin/python src/visualization/charts.py

# Collect data from Wikidata
collect:
	./venv/bin/python src/collectors/wikidata.py

# Retry 93/95 collection
retry-93-95:
	./venv/bin/python scripts/retry_93_95.py

# Clean generated files
clean:
	rm -rf docs/figures/*.png
	rm -rf data/processed/*.json
	rm -rf data/processed/*.md
	rm -rf .pytest_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Run Jupyter notebook
notebook:
	./venv/bin/jupyter notebook notebooks/

# Full pipeline
all: analyze charts test
	@echo "Pipeline complete!"

# Help
help:
	@echo "Available commands:"
	@echo "  make setup        - Create virtual environment and install deps"
	@echo "  make test         - Run tests"
	@echo "  make analyze      - Run analysis"
	@echo "  make charts       - Generate visualization charts"
	@echo "  make collect      - Collect data from Wikidata"
	@echo "  make retry-93-95  - Retry 93/95 data collection"
	@echo "  make notebook     - Start Jupyter notebook"
	@echo "  make all          - Run full pipeline"
	@echo "  make clean        - Clean generated files"

.PHONY: install format lint englishy-run-app englishy-download-preprocessed-data test-ai

install:
	uv sync

format:
	uv run ruff format .

lint:
	uv run ruff check .

englishy-run-app:
	uv run streamlit run src/englishy/app/app.py

englishy-download-preprocessed-data:
	@echo "Downloading preprocessed English learning data..."
	# TODO: Implement data download logic for English learning materials
	@echo "Data download completed."

docker-build:
	docker build -t englishy .

docker-run:
	docker run -p 8501:8501 --env-file .env englishy

docker-compose-up:
	docker-compose up --build

docker-compose-down:
	docker-compose down

test-ai:
	uv run python test_ai_modules.py

test-individual:
	uv run python test_individual_modules.py

test-module:
	@echo "Usage: make test-module MODULE=<module_name>"
	@echo "Available modules: english_extractor, grammar_analyzer, query_refiner, query_expander, outline_creater, report_writer, mindmap_maker, web_search, all"
	@if [ -n "$(MODULE)" ]; then uv run python test_specific_module.py $(MODULE); fi

test-cli:
	uv run python -m src.main search "gerunds in English" --limit 3 
# Englishy - Making English Learning Easy

## Requirements

- uv
    - `pip install uv`
- OpenAI
    - `OPENAI_API_KEY`
- GCloud CLI (optional)
    - https://cloud.google.com/sdk/docs/install

## Run

### 1. Install dependencies

Install Python packages

```shell
make install
```

### 2. Create .env file

Create .env file and put it in the repository root directory.

```text
OPENAI_API_KEY=sk-...  # OpenAI API KEY
ENGLISHY_WEB_SEARCH_ENGINE=DuckDuckGo
ENGLISHY_LM=openai/gpt-4o-mini
```

### 3. Download Preprocessed Data

```shell
make englishy-download-preprocessed-data
```

## Run App

```shell
make englishy-run-app
```

## Docker

### Build and run with Docker

```shell
make docker-build
make docker-run
```

### Or use Docker Compose

```shell
make docker-compose-up
```

## Development

### Format & Lint

format:

```shell
make format
```

lint:

```shell
make lint
```

## Features

- **English Learning Content Analysis**: Analyze English textbooks, grammar books, and learning materials
- **Web Search Integration**: Search for additional English learning resources and explanations
- **AI-Powered Reports**: Generate comprehensive English learning guides with AI
- **Mind Map Generation**: Create visual learning maps for English concepts
- **Progress Tracking**: Monitor learning progress and identify areas for improvement
- **Multi-level Content**: Support for beginner to advanced English learning materials

## Architecture

Englishy follows the same modular architecture as Lawsy, adapted for English learning:

```
src/englishy/
├── ai/          # AI models and prompt management
├── app/         # Streamlit application UI/UX
├── chunker/     # Text chunking for English content
├── encoder/     # Text embedding and vectorization
├── parser/      # English learning material parsing
├── reranker/    # Search result reranking
├── retriever/   # Information retrieval (web search, vector search)
└── utils/       # Utility functions
``` 
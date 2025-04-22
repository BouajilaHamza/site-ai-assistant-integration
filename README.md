# Site AI Assistant Integration

This project provides an AI-powered assistant for integrating with websites. It includes features for knowledge base management, language detection, and validation metrics.

## Features

- **Knowledge Base Management**: Automatically extract and manage knowledge from website sitemaps.
- **Language Detection**: Detects the language of user queries (Arabic, English, French) and uses appropriate AI models.
- **Validation Metrics**: Provides retrieval and LLM metrics for system validation.

## Project Structure

- `backend/`: Contains the core application logic, including API routes, services, and utilities.
  - `api/`: Handles API routing and request handling.
  - `core/`: Core configurations and settings.
  - `services/`: Business logic for agents, vector stores, and more.
  - `utils/`: Utility functions for parsing, validation, and language detection.
- `models/`: Stores pre-trained models like `lid.176.ftz` for language detection.
- `static/`: Static assets such as CSS, JavaScript, and images.
- `templates/`: HTML templates for the web interface.

## Setup Instructions

1. **Install `uv`**:
   ```bash
   pip install uv
   ```

2. **Create a Virtual Environment**:
   ```bash
   uv venv
   ```

3. **Sync Dependencies**:
   - For production dependencies:
     ```bash
     uv sync
     ```
   - For development dependencies (including extras):
     ```bash
     uv sync --all-extras
     ```

4. **Run the Application**:
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Access the Application**:
   Open your browser and navigate to `http://127.0.0.1:8000`.

## Validation & Experiment Tracking

- The chatbot UI includes a collapsible metrics section showing retrieval and LLM evaluation metrics (Precision, Recall, F1, ROUGE, BERTScore, etc.).
- Metrics are computed in the backend and can be optionally displayed in the UI for technical users.
- The backend is integrated with Comet ML for experiment tracking and evaluation logging.
- Metrics are not fetched/submitted on every chat message by default, but the infrastructure is in place for robust evaluation.

## Experiment Tracking

- Integrated with [Comet ML](https://www.comet.com/) for experiment tracking and evaluation logging.
- Configure your Comet ML credentials in the `.env` file:
  - `COMET_ML_API_KEY`
  - `COMET_ML_PROJECT_NAME`
  - `COMET_ML_WORKSPACE`

## Evaluation & Validation Architecture

- **Modular evaluation pipeline** under `backend/evaluation/`:
  - `rag/`: Retriever metrics and reranking (e.g., Precision@K, Recall@K, Cross-Encoder)
  - `llm/`: LLM response metrics (e.g., BERTScore, ROUGE, custom faithfulness)
  - `experiment_tracking.py`: Centralized experiment logging (Comet ML)
  - `utils.py`: Orchestration logic for evaluation and validation
  - `synthetic_data.py`: (Planned) Synthetic QA/test set generation
- **API endpoints** for both ground-truth validation and live evaluation.
- **Frontend** displays metrics in a collapsible section for technical users.

## Environment Variables

- `TARGET_DOMAIN`: The target website domain for sitemap extraction.
- `GROQ_API_KEY`: API key for Groq AI models.
- `BASE_URL`: Target website domain for sitemap extraction.
- `COMET_ML_API_KEY`, `COMET_ML_PROJECT_NAME`, `COMET_ML_WORKSPACE`: Comet ML experiment tracking.
- (Optional) `HUGGINGFACE_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY` for additional integrations.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

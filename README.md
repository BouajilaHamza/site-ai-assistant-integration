# Site AI Assistant Integration

This project provides an AI-powered assistant for integrating with websites. It includes features for knowledge base management, language detection, and validation metrics.

## Features

- **Knowledge Base Management**: Automatically extract and manage knowledge from website sitemaps.
- **Language Detection**: Detects the language of user queries (Arabic, English, French) and uses appropriate AI models.
- **Validation Metrics**: Provides retrieval and LLM metrics for system validation.

## Project Structure

- `backend/`: Contains the core application logic, including API routes, services, and utilities.
- `models/`: Stores pre-trained models like `lid.176.ftz` for language detection.
- `static/`: Static assets such as CSS, JavaScript, and images.
- `templates/`: HTML templates for the web interface.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd site-ai-assistant-integration
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Download the language detection model:
   ```bash
   python -c "from backend.services.agent_services import download_model; import asyncio; asyncio.run(download_model())"
   ```

5. Start the application:
   ```bash
   uvicorn backend.main:app --reload
   ```

6. Access the application at `http://127.0.0.1:8000`.

## Environment Variables

- `TARGET_DOMAIN`: The target website domain for sitemap extraction.
- `GROQ_API_KEY`: API key for Groq AI models.
- `HUGGINGFACE_API_KEY`: API key for Hugging Face model downloads.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

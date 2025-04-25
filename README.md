# Site AI Assistant Integration

A modern, production-ready AI assistant platform for integrating advanced language models with your website's knowledge base.  
Easily build, manage, and query a multilingual knowledge base with robust evaluation and a sleek, responsive frontend.

---

## Features

- **Knowledge Base Initialization**
  - Extracts and chunks content from your website using a base URL or sitemap file upload.
  - Semantic chunking and FAISS vector search for efficient, accurate retrieval.

- **Multilingual Language Detection**
  - Detects user query language (Arabic, English, French, etc.) using FastText.
  - Automatically adapts prompts and responses for Arabic/Persian or English.

- **LLM Integration**
  - Uses Groq's Llama-3.3-70b-versatile model for chat responses.
  - Context-aware answers based on retrieved knowledge base content.

- **Validation & Evaluation Metrics**
  - Computes retrieval metrics (Precision, Recall, F1), LLM metrics (ROUGE, BERTScore), and cross-encoder relevance.
  - Metrics are displayed in the frontend and logged to Comet ML for experiment tracking.

- **Modern Frontend**
  - Responsive Bootstrap UI with sidebar for knowledge base setup, chat, and collapsible metrics section.
  - Real-time chat and feedback.

---

## Project Structure

- `backend/`: FastAPI app, API routes, vector store, evaluation, and utilities.
- `models/`: Pre-trained FastText language detection model.
- `static/`: CSS, JS, and images for the frontend.
- `templates/`: Jinja2 HTML templates.

---

## Quickstart

1. **Install [uv](https://github.com/astral-sh/uv):**
   ```bash
   pip install uv
   ```

2. **Create a Virtual Environment:**
   ```bash
   uv venv
   ```

3. **Sync Dependencies:**
   ```bash
   uv sync --all-extras
   ```

4. **Configure Environment Variables:**  
   Copy `.env.sample` to `.env` and fill in your API keys and base URL.

5. **Run the Application:**
   ```bash
   uvicorn backend.main:app --reload
   ```

6. **Open in Browser:**  
   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## Usage

### Knowledge Base Initialization

- Use the sidebar form to enter a base URL or upload a sitemap file.
- The backend extracts, chunks, and indexes your website content for retrieval.

### Chat & Language Detection

- Enter your question in any supported language.
- The system detects the language and adapts the prompt for the LLM.
- Arabic and Persian queries get native-language prompts; others default to English.

### Validation & Experiment Tracking

- **Metrics:** Precision, Recall, F1, ROUGE, BERTScore, Cross-Encoder Relevance, Latency.
- **Comet ML Integration:**  
  - Logs all evaluation metrics and parameters for experiment tracking.
  - Configure your Comet ML credentials in `.env`.

---

## Environment Variables

- `GROQ_API_KEY`: Groq LLM API key.
- `BASE_URL`: Default website for sitemap extraction.
- `COMET_ML_API_KEY`, `COMET_ML_PROJECT_NAME`, `COMET_ML_WORKSPACE`: Comet ML tracking.
- (Optional) `HUGGINGFACE_API_KEY`, `TAVILY_API_KEY`, `FIRECRAWL_API_KEY` for extra integrations.

---

## License

MIT License.  
See [LICENSE](LICENSE) for details.

---

## Contact

For questions, suggestions, or contributions, please open an issue or pull request.

---

## Embedding the AI Assistant Widget

You can easily add the Site AI Assistant to any website with a single line of code. The widget will appear as a chat bubble in the bottom-right corner and connect to your private backend.

**Integration Snippet:**

```html
<!-- Site AI Assistant Widget -->
<script src="https://YOUR_BACKEND_URL/static/js/widget.js"></script>
```

Replace `YOUR_BACKEND_URL` with your actual backend URL or IP address.

- The widget will automatically inject a chat UI into your site.
- All chat data is sent securely to your self-hosted backend.
- For advanced configuration, see the widget source at `static/js/widget.js`.

**Note:**
- Ensure your backend allows CORS requests from your website domain.
- The backend must serve the widget at `/static/js/widget.js` and expose a chat API at `/api/chat`.

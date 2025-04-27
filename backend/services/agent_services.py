from backend.core.config import settings
from backend.utils.lang_detect_utils import MODEL_PATH
from backend.services.context_service import vector_repository
from langchain_groq import ChatGroq
import fasttext
import logging 



logger = logging.getLogger(__name__)


groq_client = ChatGroq(model="llama-3.3-70b-versatile",api_key=settings.GROQ_API_KEY)
# groq_client_allam = ChatGroq(model="allam-2-7b", api_key=settings.GROQ_API_KEY)
language_model = None

def load_language_model():
    global language_model
    if language_model is None:
        language_model = fasttext.load_model(str(MODEL_PATH))











def detect_language(text: str) -> str:
    logger.debug("Loading language model...")
    load_language_model()
    logger.debug(f"Detecting language for text: {text}")
    prediction = language_model.predict(text, k=1)  # Get the top prediction
    logger.debug(prediction)
    lang_code = prediction[0][0].replace("__label__", "")
    return lang_code


async def query_knowledge_base(question: str) -> str:
    relevant_docs = vector_repository.similarity_search(question)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    language = detect_language(question)
    logger.debug(language)
    if language in ["ar","fa"]:
        prompt = f"""بناءً على السياق التالي:
        {context}

        السؤال: {question}
        الإجابة:"""
        return await groq_client.ainvoke(prompt)
    else:
        prompt = f"""Based on the following context:
        {context}

        Question: {question}
        Answer:"""
        return await groq_client.ainvoke(prompt)



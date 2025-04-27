import time
import logging
import numpy as np
from backend.services.vectore_store import vector_store
from backend.evaluation.llm.scoring import calculate_llm_metrics
from backend.evaluation.llm.response_metrics import aggregate_bertscores
from backend.evaluation.llm.bert_utils import bert_score
from backend.evaluation.rag.retriever_metrics import calculate_retrieval_metrics
from backend.evaluation.rag.reranking import evaluate_retrieval_with_cross_encoder
from backend.evaluation.experiment_tracking import get_experiment

logger = logging.getLogger(__name__)


def get_embedding(text: str):
    return vector_store.embeddings.embed_query(text)


async def validate_rag_system(retrieved_docs, ground_truth_docs, generated_answer, reference_answer):
    logger.debug("Validating RAG system...")
    retrieval_metrics = calculate_retrieval_metrics(retrieved_docs, ground_truth_docs)
    logger.debug("Retrieval metrics calculated.")
    llm_metrics = calculate_llm_metrics(generated_answer, reference_answer)
    logger.debug("LLM metrics calculated.")
    logger.debug("RAG system validation completed.")
    return {
        "retrieval_metrics": retrieval_metrics,
        "llm_metrics": llm_metrics
    }


def evaluation_task(x):
    experiment = get_experiment()
    start_time = time.time()
    query = x.get('query')
    llm_response = x.get('llm_response')
    if not query or not llm_response:
        logger.error('Query and LLM response are required')
        return {"error": "Query and LLM response are required"}
    experiment.log_parameter("query", query)
    experiment.log_parameter("llm_response", llm_response)
    try:
        query_embedding = get_embedding(query)
        faiss_index = vector_store.vector_store.index if vector_store.vector_store else None
        if faiss_index is None:
            logger.error('FAISS index is not initialized')
            return {"error": "FAISS index is not initialized"}
        _, Index = faiss_index.search(np.asarray(query_embedding).reshape(1, -1), k=5)
        knowledge_base = [doc.page_content for doc in vector_store.vector_store.docstore._dict.values()]
        retrieved_texts = [knowledge_base[i] for i in Index[0] if i < len(knowledge_base)]
    except Exception as e:
        logger.error(f'Retrieval error: {e}')
        return {"error": f"Retrieval error: {e}"}
    bertscores = []
    for text in retrieved_texts:
        try:
            bscore = bert_score(llm_response, text)
            bertscores.append(bscore)
        except Exception as e:
            logger.warning(f'BERTScore error for text: {e}')
    aggregated_bertscore = aggregate_bertscores(bertscores)
    cross_encoder_metrics = evaluate_retrieval_with_cross_encoder(query, retrieved_texts)
    experiment.log_metric("cross_encoder_mean_relevance", cross_encoder_metrics["mean_relevance"])
    experiment.log_metric("cross_encoder_max_relevance", cross_encoder_metrics["max_relevance"])
    experiment.log_metric("cross_encoder_min_relevance", cross_encoder_metrics["min_relevance"])
    llm_metrics = calculate_llm_metrics(llm_response, query)
    retrieval_metrics = calculate_retrieval_metrics(retrieved_texts, [llm_response])
    experiment.log_metric("aggregated_bertscore", aggregated_bertscore)
    experiment.log_metric("latency", time.time() - start_time)
    for k, v in retrieval_metrics.items():
        experiment.log_metric(f"retrieval_{k}", v)
    latency = time.time() - start_time
    return {
        "query": query,
        "llm_response": llm_response,
        "retrieved_texts": retrieved_texts,
        "aggregated_bertscore": aggregated_bertscore,
        "retrieval_metrics": retrieval_metrics,
        "cross_encoder_metrics": cross_encoder_metrics,
        "llm_metrics": llm_metrics,
        "latency": latency,
    }
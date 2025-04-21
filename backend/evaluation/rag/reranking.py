from sentence_transformers import CrossEncoder

cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def rerank_with_cross_encoder(query: str, retrieved_docs: list) -> list:
    pairs = [[query, doc] for doc in retrieved_docs]
    scores = cross_encoder.predict(pairs)
    reranked = sorted(zip(retrieved_docs, scores), key=lambda x: x[1], reverse=True)
    return reranked

def evaluate_retrieval_with_cross_encoder(query: str, retrieved_docs: list) -> dict:
    pairs = [[query, doc] for doc in retrieved_docs]
    scores = cross_encoder.predict(pairs)
    scores = list(map(float, scores))
    return {
        "mean_relevance": float(sum(scores) / len(scores)) if len(scores) > 0 else 0.0,
        "max_relevance": float(max(scores)) if len(scores) > 0 else 0.0,
        "min_relevance": float(min(scores)) if len(scores) > 0 else 0.0,
        "scores": scores,
    }

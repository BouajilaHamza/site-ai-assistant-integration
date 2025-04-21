from typing import List, Dict
from sklearn.metrics import precision_score, recall_score, f1_score

def calculate_retrieval_metrics(retrieved_docs: List[str], ground_truth_docs: List[str]) -> Dict[str, float]:
    """
    Calculate retrieval metrics: Precision, Recall, and F1-score.
    Args:
        retrieved_docs (List[str]): List of retrieved document URLs.
        ground_truth_docs (List[str]): List of ground truth document URLs.
    Returns:
        Dict[str, float]: Dictionary containing precision, recall, and F1-score.
    """
    y_true = [1 if doc in ground_truth_docs else 0 for doc in retrieved_docs]
    y_pred = [1] * len(retrieved_docs)
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    return {"precision": precision, "recall": recall, "f1_score": f1}

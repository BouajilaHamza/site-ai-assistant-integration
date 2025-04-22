from typing import List

def aggregate_bertscores(bertscores: List[dict]) -> float:
    """
    Aggregate BERTScore results (mean of F1 scores).
    Args:
        bertscores (List[dict]): List of BERTScore dicts with 'f1_score'.
    Returns:
        float: Mean F1 score, or 0.0 if empty.
    """
    if not bertscores:
        return 0.0
    return sum([score['f1_score'] for score in bertscores]) / len(bertscores)

from typing import List, Dict
from sklearn.metrics import precision_score, recall_score, f1_score
from rouge_score import rouge_scorer
import torch
from transformers import BertTokenizer, BertModel
import logging

# Load BERT model and tokenizer
MODEL_NAME = "bert-base-uncased"

tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME, device_map="auto")


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.info)


def get_embeddings(text):
    """
    Generate token embeddings for the input text using BERT.

    Args:
        text (str): Input text or batch of sentences.

    Returns:
        torch.Tensor: Token embeddings with shape (batch_size, seq_len, hidden_dim).
    """
    # Tokenize input text
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    # Move inputs to GPU if available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = inputs.to(device)

    # Compute embeddings without gradient calculation
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    # Return last hidden states (token-level embeddings)
    return outputs.last_hidden_state


def cosine_similarity(generated_embeddings, reference_embeddings):
    """
    Compute cosine similarity between two sets of embeddings.

    Args:
        generated_embeddings (torch.Tensor): Embeddings of candidate tokens with shape (batch_size, seq_len, hidden_dim).
        reference_embeddings (torch.Tensor): Embeddings of reference tokens with shape (batch_size, seq_len, hidden_dim).

    Returns:
        torch.Tensor: Cosine similarity matrix with shape (seq_len_generated, seq_len_reference).
    """
    # Normalize embeddings along the hidden dimension
    generated_embeddings = torch.nn.functional.normalize(generated_embeddings, dim=-1)
    reference_embeddings = torch.nn.functional.normalize(reference_embeddings, dim=-1)

    # Compute similarity using batched matrix multiplication
    return torch.bmm(generated_embeddings, reference_embeddings.transpose(1, 2))



def get_precision(similarity_matrix):
    """
    Calculate BERT precision as the mean of the maximum similarity scores from the candidate to the reference.

    Args:
        similarity_matrix (torch.Tensor): Cosine similarity matrix.

    Returns:
        torch.Tensor: Precision score.
    """
    return similarity_matrix.max(dim=2)[0].mean()



def get_recall(similarity_matrix):
    """
    Calculate BERT recall as the mean of the maximum similarity scores from the reference to the candidate.

    Args:
        similarity_matrix (torch.Tensor): Cosine similarity matrix.

    Returns:
        torch.Tensor: Recall score.
    """
    return similarity_matrix.max(dim=1)[0].mean()


def get_f1_score(precision, recall):
    """
    Compute the F1 score given precision and recall.

    Args:
        precision (torch.Tensor): Precision score.
        recall (torch.Tensor): Recall score.

    Returns:
        torch.Tensor: F1 score.
    """
    return 2 * (precision * recall) / (precision + recall)




def bert_score(candidate, reference):
    """
    Compute BERTScore (Precision, Recall, F1) between a candidate and a reference sentence.

    Args:
        candidate (str): Candidate sentence.
        reference (str): Reference sentence.

    Returns:
        dict: Dictionary containing precision, recall, and F1 scores.
    """
    # Get token embeddings for candidate and reference
    candidate_embeddings = get_embeddings(candidate)
    reference_embeddings = get_embeddings(reference)

    # Compute cosine similarity matrix
    similarity_matrix = cosine_similarity(candidate_embeddings, reference_embeddings)

    # Calculate precision, recall, and F1 scores
    precision = get_precision(similarity_matrix)
    recall = get_recall(similarity_matrix)
    f1_score = get_f1_score(precision, recall)

    # Return scores as a dictionary
    return {
        "precision": precision.item(),
        "recall": recall.item(),
        "f1_score": f1_score.item(),
    }





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

def calculate_llm_metrics(generated_answer: str, reference_answer: str) -> Dict[str, float]:
    """
    Calculate LLM response metrics: ROUGE and BERTScore.

    Args:
        generated_answer (str): The answer generated by the LLM.
        reference_answer (str): The reference (ground truth) answer.

    Returns:
        Dict[str, float]: Dictionary containing ROUGE and BERTScore metrics.
    """
    # ROUGE
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)
    logger.debug(f"Calculating ROUGE scores for generated answer: {generated_answer}")
    rouge_scores = rouge.score(reference_answer, generated_answer)
    logger.debug(f"ROUGE scores: {rouge_scores}")
    # BERTScore
    logger.debug("Calculating BERTScore for generated answer: ")
    scores = bert_score(generated_answer, reference_answer)
    return {
        "rouge1": rouge_scores['rouge1'].fmeasure,
        "rougeL": rouge_scores['rougeL'].fmeasure,
        "bert_score": scores
    }
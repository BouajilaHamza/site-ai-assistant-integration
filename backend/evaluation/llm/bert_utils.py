import torch
from transformers import BertTokenizer, BertModel

MODEL_NAME = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertModel.from_pretrained(MODEL_NAME)

def get_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    inputs = inputs.to(device)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    return outputs.last_hidden_state

def cosine_similarity(generated_embeddings, reference_embeddings):
    generated_embeddings = torch.nn.functional.normalize(generated_embeddings, dim=-1)
    reference_embeddings = torch.nn.functional.normalize(reference_embeddings, dim=-1)
    return torch.bmm(generated_embeddings, reference_embeddings.transpose(1, 2))

def get_precision(similarity_matrix):
    return similarity_matrix.max(dim=2)[0].mean()

def get_recall(similarity_matrix):
    return similarity_matrix.max(dim=1)[0].mean()

def get_f1_score(precision, recall):
    return 2 * (precision * recall) / (precision + recall)

def bert_score(candidate, reference):
    candidate_embeddings = get_embeddings(candidate)
    reference_embeddings = get_embeddings(reference)
    similarity_matrix = cosine_similarity(candidate_embeddings, reference_embeddings)
    precision = get_precision(similarity_matrix)
    recall = get_recall(similarity_matrix)
    f1_score = get_f1_score(precision, recall)
    return {
        "precision": precision.item(),
        "recall": recall.item(),
        "f1_score": f1_score.item(),
    }

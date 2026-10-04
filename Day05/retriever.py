from embeding import create_embedding
from similarity import cosine_similarity

def retrieve(question, documents=None):
    question = question.lower()
    qestion_embedding = create_embedding(question)
    similarities = [];
    for filename, content in documents.items():
        content_embedding = create_embedding(content)
        similarity_score = cosine_similarity(qestion_embedding, content_embedding)
        similarity = {"filename": filename, "similarity": similarity_score, "content": content}
        similarities.append(similarity)
    max_similarity = max(similarities, key=lambda x: x["similarity"])
    return max_similarity

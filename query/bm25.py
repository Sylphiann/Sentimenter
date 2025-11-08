import bm25s
from .models import Sentence

def search_sentences_bm25(query: str, top_k: int = 15):
    all_sentences = Sentence.objects.all()
    corpus = [sentence.sentence for sentence in all_sentences]

    if not corpus:
        return []

    sentence_map = list(all_sentences)
    corpus_tokens = bm25s.tokenize(corpus)
    
    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    query_tokens = bm25s.tokenize([query])
    doc_ids, scores = retriever.retrieve(query_tokens, k=top_k)

    # Flatten
    ranked_indices = doc_ids[0]
    ranked_scores = scores[0]

    ranked_results = []
    for index, score in zip(ranked_indices, ranked_scores):
        # Only if a result scores > 0.0
        if score > 0:
            sentence_instance = sentence_map[index]
            ranked_results.append((int(sentence_instance.id), sentence_instance, score))

    return ranked_results
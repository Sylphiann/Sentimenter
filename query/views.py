from django.shortcuts import render
from .bm25 import search_sentences_bm25

# Create your views here.

def main_view(request):
    return render(request, 'main.html')

def search_result(request):
    query = request.GET.get('q', '').strip()

    results = []
    if query:
        results = search_sentences_bm25(query, top_k=10)

    context = {
        'query': query,
        'results': results, 
    }
    return render(request, 'query/result.html', context)
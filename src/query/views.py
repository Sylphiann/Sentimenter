from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from .bm25 import search_sentences_bm25
from .models import (
    Query,
    get_or_create_query,
    get_query_by_text,
    get_sentence_by_id,
    get_sentiment_by_query_and_sentence,
    create_sentiment,
    delete_sentiment_by_id
)


def main_view(request):
    return render(request, 'main.html')


def search_result(request):
    user_query = request.GET.get('q', '').strip()
    sentiment_results, sentence_results = [], []
    context = {}

    if user_query:
        new_query, _ = get_or_create_query(user_query)

        results = search_sentences_bm25(user_query, top_k=10)
        if len(results) > 0:
            for result in results:
                sentiment = get_sentiment_by_query_and_sentence(new_query, result[1])

                if sentiment:
                    sentiment_results.append((
                        sentiment.id,
                        sentiment.sentence,
                        sentiment.relation
                    ))
                else:
                    sentence_results.append(result)

        context = {
            'query': user_query,
            'sentence_results': sentence_results,
            'sentiment_results': sentiment_results
        }
    return render(request, 'query/result.html', context)


def set_sentiment(request):
    user_query = request.POST.get('user_query').strip()
    sentence_id = request.POST.get('sentence_id')
    sentiment_value = request.POST.get('sentiment_value')

    query = get_query_by_text(user_query)
    if query:
        sentence = get_sentence_by_id(sentence_id)
        if sentence:
            create_sentiment(query, sentence, sentiment_value)
        else:
            raise Query.DoesNotExist(f"Sentence with ID {sentence_id} does not exist.")
    else:
        raise Query.DoesNotExist(f"Instance query:\"{user_query}\" does not exist. Probably an encoding problem.")

    base_url = reverse('query')
    query_params = {'q': user_query}
    encoded_params = urlencode(query_params)
    redirect_url = f"{base_url}?{encoded_params}"
    return redirect(redirect_url)


def remove_sentiment(request):
    user_query = request.POST.get('user_query').strip()
    sentiment_id = request.POST.get('sentiment_id')
    delete_sentiment_by_id(sentiment_id)

    base_url = reverse('query')
    query_params = {'q': user_query}
    encoded_params = urlencode(query_params)
    redirect_url = f"{base_url}?{encoded_params}"
    return redirect(redirect_url)
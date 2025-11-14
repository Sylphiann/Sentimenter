from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import urlencode
from .bm25 import search_sentences_bm25
from .models import Query, Sentiment, get_sentiment_if_exists, get_query_if_exists, get_sentence_by_id, delete_sentiment_by_id

# Create your views here.

def main_view(request):
    return render(request, 'main.html')


def search_result(request):
    user_query = request.GET.get('q', '').strip()
    sentiment_results, sentence_results = [], []
    context = {}

    if user_query:
        new_query, _ = Query.objects.get_or_create(
            query=user_query
        )

        results = search_sentences_bm25(user_query, top_k=10)
        if len(results) > 0:
            for result in results:
                sentiment: Sentiment = get_sentiment_if_exists(new_query, result[1])

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

    get_query = get_query_if_exists(user_query)
    if get_query:
        get_sentence = get_sentence_by_id(sentence_id)
        Sentiment.objects.create(
            query=get_query,
            sentence=get_sentence,
            relation=sentiment_value
        ) 
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
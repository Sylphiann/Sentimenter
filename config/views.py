from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
import json
from query.models import Sentence, Query, Sentiment, get_query_by_id, delete_sentiment_by_id


@staff_member_required
def admin_sentence_view(request):
    """
    Handles both bulk import of sentences from a .txt file and 
    export of all Sentence instances as JSON. Accessible only to superusers.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have the required permissions of a superuser status to access this tool.")

    context = {}
    context['sentence_list'] = list(Sentence.objects.values_list('id', 'sentence'))
    
    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'import_sentences':
            if 'sentences_file' in request.FILES:
                uploaded_file = request.FILES['sentences_file']
                
                if not uploaded_file.name.endswith('.txt'):
                    context['error'] = 'Invalid file format. Please upload a .txt file.'
                else:
                    try:
                        file_data = uploaded_file.read().decode('utf-8')
                        sentences = []
                        for line in file_data.splitlines():
                            text = line.strip()
                            if text:
                                sentences.append(Sentence(sentence=text))

                        Sentence.objects.bulk_create(sentences)
                        context['success'] = f'Successfully imported {len(sentences)} sentences.'
                    
                    except Exception as e:
                        context['error'] = f'An error occurred during import: {e}'
            else:
                context['error'] = 'No file was uploaded for import.'
        

        elif action == 'delete_sentences':
            all_sentences = Sentence.objects.all()
            deleted_count, _ = all_sentences.delete()
            context['success'] = f'Successfully deleted {deleted_count} sentences.'
        

        elif action == 'delete_a_sentence':
            try:
                sentence_id = request.POST.get('sentence_id')
                sentence = Sentence.objects.get(id=sentence_id)
                sentence.delete()
                context['success'] = f"Sentence with ID {sentence_id} successfully deleted."

            except Sentence.DoesNotExist:
                context['error'] = f"Error: Sentence with ID {sentence_id} not found."
        
        return redirect('admin-sentence')
    
    return render(request, 'config/config-sentence.html', context)



@staff_member_required
def admin_sentiment_view(request):
    """
    Handles both bulk import of sentences from a .txt file and 
    export of all Sentence instances as JSON. Accessible only to superusers.
    """
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have the required permissions of a superuser status to access this tool.")

    context = {}
    context['all_sentiments'] = []

    queries = Query.objects.all().prefetch_related('related_queries')
    
    for query in queries:
        sentence_relations = []
        for sentiment_object in query.related_queries.all():
            sentence_relations.append({
                'sentence_id': sentiment_object.sentence.id,
                'sentence_text': sentiment_object.sentence.sentence,
                'relation': sentiment_object.relation,
                'sentiment_id': sentiment_object.id,
            })
        
        query_entry = {
            'query_id': query.id,
            'query_text': query.query,
            'related_entries': sentence_relations,
        }
        
        context['all_sentiments'].append(query_entry)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == "export_sentiments":
            sentiments = Sentiment.objects.all().select_related('sentence', 'query')
            data_list = []

            for sentiment_obj in sentiments:
                data_list.append({
                    'query': sentiment_obj.query.query,
                    'sentence': sentiment_obj.sentence.sentence,
                    'relation': sentiment_obj.get_relation_display(), 
                })
            data = json.dumps(data_list, indent=4)
            
            response = HttpResponse(data, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="all_sentiments.json"'
            
            return response
        
        elif action == "delete_all_sentiments":
            Sentiment.objects.all().delete()
            Query.objects.all().delete()

        elif action == "delete_a_query":
            query_id = request.POST.get('query_id')
            delete_query = get_query_by_id(query_id)
            delete_query.delete()

        elif action == "remove_a_sentiment":
            sentiment_id = request.POST.get('sentiment_id')
            delete_sentiment_by_id(sentiment_id)

        return redirect('admin-sentiment')

    return render(request, 'config/config-sentiment.html', context)
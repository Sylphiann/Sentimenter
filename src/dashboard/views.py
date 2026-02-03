from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
import json
from query.models import (
    get_all_sentences,
    create_sentences_bulk,
    delete_sentence_by_id,
    delete_all_sentences,
    get_all_queries,
    delete_query_by_id,
    get_all_sentiments,
    delete_sentiment_by_id,
    delete_all_sentiments,
    delete_all_queries
)


@staff_member_required
def admin_sentence_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have the required permissions of a superuser status to access this tool.")

    context = {}
    context['sentence_list'] = list(get_all_sentences().values_list('id', 'sentence'))
    
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
                        sentences_data = [line.strip() for line in file_data.splitlines() if line.strip()]
                        
                        if sentences_data:
                            create_sentences_bulk(sentences_data)
                            context['success'] = f'Successfully imported {len(sentences_data)} sentences.'
                        else:
                            context['error'] = 'No valid sentences found in the file.'
                    
                    except Exception as e:
                        context['error'] = f'An error occurred during import: {e}'
            else:
                context['error'] = 'No file was uploaded for import.'
        

        elif action == 'delete_sentences':
            deleted_count = delete_all_sentences()
            context['success'] = f'Successfully deleted {deleted_count} sentences.'
        

        elif action == 'delete_a_sentence':
            sentence_id = request.POST.get('sentence_id')
            if delete_sentence_by_id(sentence_id):
                context['success'] = f"Sentence with ID {sentence_id} successfully deleted."
            else:
                context['error'] = f"Error: Sentence with ID {sentence_id} not found."
        
        return redirect('admin-sentence')
    
    return render(request, 'dashboard/dashboard-sentence.html', context)



@staff_member_required
def admin_sentiment_view(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have the required permissions of a superuser status to access this tool.")

    context = {}
    context['all_sentiments'] = []

    queries = get_all_queries()
    
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
            sentiments = get_all_sentiments()
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
            delete_all_sentiments()
            delete_all_queries()

        elif action == "delete_a_query":
            query_id = request.POST.get('query_id')
            delete_query_by_id(query_id)

        elif action == "remove_a_sentiment":
            sentiment_id = request.POST.get('sentiment_id')
            delete_sentiment_by_id(sentiment_id)

        return redirect('admin-sentiment')

    return render(request, 'dashboard/dashboard-sentiment.html', context)
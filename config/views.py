from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.admin.views.decorators import staff_member_required
from django.core.serializers import serialize
from query.models import Sentence


@staff_member_required
def admin_tools_view(request):
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
            
            return redirect('admin-sentence')


        elif action == 'export_sentences':
            data = serialize('json', Sentence.objects.all(), fields=('text', 'sentiment'))
            response = HttpResponse(data, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="all_sentences.json"'
            
            return response


        elif action == 'delete_sentences':
            all_sentences = Sentence.objects.all()
            deleted_count, _ = all_sentences.delete()
            context['success'] = f'Successfully deleted {deleted_count} sentences.'

            return redirect('admin-sentence')
        

        elif action == 'delete_a_sentence':
            try:
                sentence_id = request.POST.get('sentence_id')
                sentence = Sentence.objects.get(id=sentence_id)
                sentence.delete()
                context['success'] = f"Sentence with ID {sentence_id} successfully deleted."

            except Sentence.DoesNotExist:
                context['error'] = f"Error: Sentence with ID {sentence_id} not found."

            return redirect('admin-sentence')
        
        return render(request, 'config/config.html', context)
    
    return render(request, 'config/config.html', context)
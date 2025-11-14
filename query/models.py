from django.db import models

class Sentence(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return self.sentence
    

class Query(models.Model):
    query = models.TextField()

    def __str__(self):
        return self.query


class Sentiment(models.Model):
    SENTIMENT_CHOICES = [
        ('agreement', 'Agreement'),
        ('disagreement', 'Disagreement'),
        ('no_relation', 'No Relation'),
    ]

    query = models.ForeignKey(Query, related_name='related_queries', on_delete=models.CASCADE)
    sentence = models.ForeignKey(Sentence, related_name='related_sentences', on_delete=models.CASCADE)
    relation = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        default='no_relation'
    )
    
    def __str__(self):
        return self.text[:50]

    class Meta:
        # Newest sentence shown first
        ordering = ['-id']


# Helper methods

def get_all_sentences():
    queryset = Sentence.objects.all()
    return queryset


def get_sentiment_if_exists(query: Query, sentence: Sentence):
    try:
        sentiment = Sentiment.objects.get(
            query = query,
            sentence = sentence
        )
        return sentiment
    except Sentiment.DoesNotExist:
        return None
    

def get_query_if_exists(user_query: str):
    try:
        query = Query.objects.get(query=user_query)
        return query   
    except Query.DoesNotExist:
        return None
    

def get_sentence_by_id(sentence_id: int):
    try:
        sentence = Sentence.objects.get(pk=sentence_id)
        return sentence   
    except Sentence.DoesNotExist:
        return None
    

def get_query_by_id(query_id: int):
    try:
        query = Query.objects.get(pk=query_id)
        return query   
    except Query.DoesNotExist:
        return None


def delete_sentiment_by_id(sentiment_id: int):
    try:
        sentiment = Sentiment.objects.get(pk=sentiment_id)
        sentiment.delete()
        
    except Sentiment.DoesNotExist:
        return None
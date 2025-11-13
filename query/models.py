from django.db import models

class Sentiment(models.Model):
    SENTIMENT_CHOICES = [
        ('agreement', 'Agreement'),
        ('disagreement', 'Disagreement'),
        ('no_relation', 'No Relation'),
    ]

    query = models.TextField()
    sentence = models.TextField()
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


class Sentence(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return self.sentence
    

class Query(models.Model):
    sentence = models.TextField()

    def __str__(self):
        return self.sentence


def get_all_sentences():
    queryset = Sentence.objects.all()
    return queryset


def get_sentiment_if_exists(query: Query, sentence: Sentence):
    try:
        print(f"{type(query)} : {type(sentence)}")
        sentiment = Sentiment.objects.get(
            query = query,
            sentence = sentence
        )
        return sentiment
    except Sentiment.DoesNotExist:
        return None
    

def get_query_if_exists(user_query: str):
    try:
        query = Query.objects.get(sentence=user_query)
        return query   
    except Query.DoesNotExist:
        return None
    

def get_sentence_by_id(sentence_id: int):
    try:
        sentence = Sentence.objects.get(pk=sentence_id)
        return sentence   
    except Sentence.DoesNotExist:
        return None
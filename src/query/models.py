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
        ordering = ['-id']


def get_all_sentences():
    return Sentence.objects.all()


def get_sentence_by_id(sentence_id: int):
    try:
        return Sentence.objects.get(pk=sentence_id)
    except Sentence.DoesNotExist:
        return None


def create_sentence(sentence_text: str):
    return Sentence.objects.create(sentence=sentence_text)


def create_sentences_bulk(sentences_data: list):
    sentences = [Sentence(sentence=text) for text in sentences_data]
    return Sentence.objects.bulk_create(sentences)


def delete_sentence_by_id(sentence_id: int):
    try:
        sentence = Sentence.objects.get(pk=sentence_id)
        sentence.delete()
        return True
    except Sentence.DoesNotExist:
        return False


def delete_all_sentences():
    deleted_count, _ = Sentence.objects.all().delete()
    return deleted_count


def get_all_queries():
    return Query.objects.all().prefetch_related('related_queries')


def get_query_by_id(query_id: int):
    try:
        return Query.objects.get(pk=query_id)
    except Query.DoesNotExist:
        return None


def get_query_by_text(query_text: str):
    try:
        return Query.objects.get(query=query_text)
    except Query.DoesNotExist:
        return None


def get_or_create_query(query_text: str):
    return Query.objects.get_or_create(query=query_text)


def delete_query_by_id(query_id: int):
    try:
        query = Query.objects.get(pk=query_id)
        query.delete()
        return True
    except Query.DoesNotExist:
        return False


def delete_all_queries():
    deleted_count, _ = Query.objects.all().delete()
    return deleted_count


def get_all_sentiments():
    return Sentiment.objects.all().select_related('query', 'sentence')


def get_sentiment_by_id(sentiment_id: int):
    try:
        return Sentiment.objects.get(pk=sentiment_id)
    except Sentiment.DoesNotExist:
        return None


def get_sentiment_by_query_and_sentence(query: Query, sentence: Sentence):
    try:
        return Sentiment.objects.get(query=query, sentence=sentence)
    except Sentiment.DoesNotExist:
        return None


def create_sentiment(query: Query, sentence: Sentence, relation: str):
    return Sentiment.objects.create(
        query=query,
        sentence=sentence,
        relation=relation
    )


def delete_sentiment_by_id(sentiment_id: int):
    try:
        sentiment = Sentiment.objects.get(pk=sentiment_id)
        sentiment.delete()
        return True
    except Sentiment.DoesNotExist:
        return False


def delete_all_sentiments():
    deleted_count, _ = Sentiment.objects.all().delete()
    return deleted_count
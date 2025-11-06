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


def get_all_sentences():
    queryset = Sentence.objects.all()
    return queryset
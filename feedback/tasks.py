from celery import shared_task
from .models import Feedback

@shared_task
def find_sentiment(pk, body):
    feedback = Feedback.objects.get(pk=pk)
    feedback.sentiment = "awesome"
    feedback.save()

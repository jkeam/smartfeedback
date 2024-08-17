from django.db import models

class Feedback(models.Model):
  body = models.TextField(default='', max_length=5120, null=False, blank=True)
  sentiment = models.CharField(max_length=512, null=False, blank=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False)
  updated_at = models.DateTimeField(auto_now=True, null=False)
  class Meta:
    ordering = ['-id']

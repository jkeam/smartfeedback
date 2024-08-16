from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
  context = {}
  return render(request, 'feedback/index.html', context)

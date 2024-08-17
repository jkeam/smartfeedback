from django.shortcuts import render
from .forms import UserForm, PasswordForm, FeedbackForm
from .models import Feedback
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

def home(request):
  if not request.user.is_authenticated:
    return HttpResponseRedirect("/")
  return HttpResponseRedirect(reverse('feedback:feedback-listing'))

class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    paginate_by = 100

class FeedbackDetailView(LoginRequiredMixin, DetailView):
    model = Feedback

class FeedbackUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Feedback
    form_class = FeedbackForm
    def get_success_url(self):
      return reverse('feedback:feedback-detail', kwargs={"pk": self.object.pk})

class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    success_message = 'Thanks for the feedback!'
    def get_success_url(self):
        if not self.request.user.is_authenticated:
            return "/"
        else:
            return reverse('feedback:feedback-detail', kwargs={"pk": self.object.pk})

class FeedbackDeleteView(DeleteView):
    model = Feedback
    success_url = reverse_lazy('feedback:feedback-listing')

class ChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordForm
    template_name = 'registration/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('feedback:profile-password')

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserForm
    success_message = "Successfully Updated Your Profile"
    success_url = reverse_lazy('feedback:profile-detail')
    def get_object(self, *args, **kwargs):
        return self.request.user

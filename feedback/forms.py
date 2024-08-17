from django import forms
from .models import Feedback
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class FeedbackForm(forms.ModelForm):
    body = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={'placeholder': 'Comment', 'class': 'textarea'}
    ))
    class Meta:
        model = Feedback
        fields = ['body']

class PasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(
            attrs={'placeholder': '', 'class': 'input'}
    ))

    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(
            attrs={'placeholder': '', 'class': 'input'}
    ))

    new_password2 = forms.CharField(
        label="New Password Confirmation",
        widget=forms.PasswordInput(
            attrs={'placeholder': '', 'class': 'input'}
    ))

class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username', 'class': 'input'}
    ))

    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'First Name', 'class': 'input'}
    ))

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Last Name', 'class': 'input'}
    ))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

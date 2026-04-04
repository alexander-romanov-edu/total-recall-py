from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Collection, Word


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name"]


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["text", "translation"]


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

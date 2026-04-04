from django import forms
from .models import Collection, Word
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

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

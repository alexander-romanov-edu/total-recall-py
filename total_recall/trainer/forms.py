from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from trainer.models import Collection, Word

User = get_user_model()


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name"]


class WordForm(forms.ModelForm):
    class Meta:
        model = Word
        fields = ["text", "translation"]


# pylint: disable=too-many-ancestors
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")

from django.contrib import admin

from .models import Collection, Progress, Word
from django.contrib.auth.models import User, Group

admin.site.register(Collection)
admin.site.register(Word)
admin.site.register(Progress)

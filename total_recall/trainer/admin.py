from django.contrib import admin

from .models import Collection, Progress, Word

admin.site.register(Collection)
admin.site.register(Word)
admin.site.register(Progress)

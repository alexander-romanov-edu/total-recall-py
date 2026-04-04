from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Collection(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    # null=True + blank=True → admin-created collections have owner=None

    def __str__(self):
        return self.name

class Word(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    translation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.text

class Progress(models.Model):
    word = models.OneToOneField(Word, on_delete=models.CASCADE)
    next_review = models.DateTimeField(default=now)
    interval = models.IntegerField(default=1)
    correct_streak = models.IntegerField(default=0)

    def update(self, correct: bool):
        if correct:
            self.correct_streak += 1
            self.interval *= 2
        else:
            self.correct_streak = 0
            self.interval = 1

        self.next_review = now() + timedelta(days=self.interval)
        self.save()

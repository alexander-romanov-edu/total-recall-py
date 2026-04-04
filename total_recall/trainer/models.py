from datetime import timedelta

from django.db import models
from django.utils.timezone import now


class Collection(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Word(models.Model):
    text = models.CharField(max_length=100)
    translation = models.CharField(max_length=100)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.text} - {self.translation}"


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

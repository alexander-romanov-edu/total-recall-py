import random

from django.shortcuts import redirect, render
from django.utils.timezone import now

from .models import Collection, Progress, Word
from .utils import mask_word


def get_next_word(collection):
    due_words = collection.word_set.filter(progress__next_review__lte=now())

    if due_words.exists():
        return random.choice(list(due_words))
    return random.choice(list(collection.word_set.all()))


def start(request):
    if request.method == "POST":
        request.session["score"] = 0
        request.session["total"] = 0
        request.session["collection_id"] = request.POST["collection"]
        return redirect("train")

    return render(request, "start.html", {"collections": Collection.objects.all()})


def train(request):
    collection_id = request.session.get("collection_id")
    if not collection_id:
        return redirect("start")

    collection = Collection.objects.get(id=collection_id)
    feedback = None

    if request.method == "POST":
        answer = request.POST["answer"]
        correct_word = request.session["current_word"]

        request.session["total"] += 1

        if answer.lower() == correct_word.lower():
            request.session["score"] += 1
            feedback = "Correct!"
            correct = True
        else:
            feedback = f"Wrong! Answer: {correct_word}"
            correct = False

        word = Word.objects.get(text=correct_word)
        progress, _ = Progress.objects.get_or_create(word=word)
        progress.update(correct)

    word = get_next_word(collection)
    request.session["current_word"] = word.text

    return render(
        request,
        "train.html",
        {
            "masked": mask_word(word.text),
            "translation": word.translation,
            "score": request.session["score"],
            "total": request.session["total"],
            "feedback": feedback,
        },
    )

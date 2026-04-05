import random

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .forms import CollectionForm, SignUpForm, WordForm
from .models import Collection, Progress, Word
from .utils import mask_word


def list_collections(request):
    if request.user.is_authenticated:
        collections = Collection.objects.filter(owner=None) | Collection.objects.filter(
            owner=request.user
        )
    else:
        collections = Collection.objects.filter(owner=None)

    return render(request, "list_collections.html", {"collections": collections})


def intro(request):
    collection_id = request.GET.get("collection_id")
    if collection_id:
        request.session["collection_id"] = collection_id
    return render(request, "intro.html")


def view_collection(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)
    if collection.owner and collection.owner != request.user:
        return render(request, "permission_denied.html")
    words = collection.word_set.all()
    return render(
        request,
        "view_collection.html",
        {
            "collection": collection,
            "words": words,
        },
    )


@login_required
def create_collection(request):
    if request.method == "POST":
        form = CollectionForm(request.POST)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.owner = request.user
            collection.save()
            return redirect("list_collections")
    else:
        form = CollectionForm()
    return render(request, "create_collection.html", {"form": form})


def add_word(request, collection_id):
    collection = get_object_or_404(Collection, id=collection_id)

    if collection.owner and collection.owner != request.user:
        return render(request, "permission_denied.html")

    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save(commit=False)
            word.collection = collection
            word.save()
            return redirect("view_collection", collection_id=collection.id)
    else:
        form = WordForm()

    return render(request, "add_word.html", {"form": form, "collection": collection})


def get_next_word(collection):
    due_words = collection.word_set.filter(progress__next_review__lte=now())

    if due_words.exists():
        return random.choice(list(due_words))
    return random.choice(list(collection.word_set.all()))


# TODO: make this configurable
MAX_TASKS = 10


def train(request):
    print("SESSION:", dict(request.session))
    collection_id = request.GET.get("collection_id") or request.session.get(
        "collection_id"
    )
    if not collection_id:
        return redirect("list_collections")

    collection = Collection.objects.get(id=collection_id)
    request.session["collection_id"] = collection.id
    if "score" not in request.session or "total" not in request.session:
        request.session["score"] = 0
        request.session["total"] = 0
        request.session["mistakes"] = []

    feedback = None

    if request.method == "POST":
        answer = request.POST["answer"]
        correct_word = request.session["current_word"]
        request.session["total"] += 1

        word_obj = Word.objects.get(text=correct_word, collection=collection)
        correct = answer.lower() == correct_word.lower()

        if correct:
            request.session["score"] += 1
            feedback = "Correct!"
        else:
            feedback = f"Wrong! Answer: {correct_word}"
            mistakes = request.session.get("mistakes", [])
            if not any(m["text"] == word_obj.text for m in mistakes):
                mistakes.append(
                    {"text": word_obj.text, "translation": word_obj.translation}
                )
            request.session["mistakes"] = mistakes

        progress, _ = Progress.objects.get_or_create(word=word_obj)
        progress.update(correct)

    if request.session["total"] >= MAX_TASKS:
        mistake_words = request.session.get("mistakes", [])
        score = request.session["score"]
        total = request.session["total"]
        response = render(
            request,
            "end.html",
            {
                "score": score,
                "total": total,
                "mistakes": mistake_words,
                "collection": collection,
            },
        )
        request.session.pop("score", None)
        request.session.pop("total", None)
        request.session.pop("mistakes", None)
        request.session.pop("current_word", None)
        return response
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
            "collection": collection,
        },
    )


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("list_collections")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

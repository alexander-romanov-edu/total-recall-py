from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_collections, name="list_collections"),
    path("signup/", views.signup, name="signup"),
    path('train/', views.train, name='train'),
    path("intro/", views.intro, name="intro"),
    path("collections/create/", views.create_collection, name="create_collection"),
    path("collections/<int:collection_id>/add_word/", views.add_word, name="add_word"),
    path("collections/<int:collection_id>/", views.view_collection, name="view_collection"),
]

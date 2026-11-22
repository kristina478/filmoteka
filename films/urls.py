from django.urls import path
from .views import add_review

from .views import (
    FilmListView,
    FilmDetailView,
    FilmCreateView,
    FilmUpdateView,
    FilmDeleteView,
)

urlpatterns = [
    path('', FilmListView.as_view(), name='film_list'),

    path(
        'film/<int:pk>/',
        FilmDetailView.as_view(),
        name='film_detail'
    ),

    path(
        'film/create/',
        FilmCreateView.as_view(),
        name='film_create'
    ),

    path(
        'film/<int:pk>/update/',
        FilmUpdateView.as_view(),
        name='film_update'
    ),

    path(
        'film/<int:pk>/delete/',
        FilmDeleteView.as_view(),
        name='film_delete'
    ),

    path(
    'film/<int:pk>/review/',
    add_review,
    name='add_review'
    ),
]
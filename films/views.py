from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Film, Review
from .forms import FilmForm, ReviewForm
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Prefetch

class FilmListView(ListView):
    model = Film
    template_name = 'films/film_list.html'
    context_object_name = 'films'
    paginate_by = 10

    def get_queryset(self):
        queryset = Film.objects.select_related(
            'genre',
            'author'
        ).prefetch_related(
            'actors'
)

        search = self.request.GET.get('search')
        genre = self.request.GET.get('genre')
        status = self.request.GET.get('status')

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        if genre:
            queryset = queryset.filter(
                genre_id=genre
            )

        if status:
            queryset = queryset.filter(
                status=status
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        from .models import Genre

        context['genres'] = Genre.objects.all()

        return context

class FilmDetailView(DetailView):
    model = Film

    queryset = Film.objects.select_related(
        'genre',
        'author'
    ).prefetch_related(
        'actors',
        'reviews'
    )
    template_name = 'films/film_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        film = self.object

        context['reviews'] = film.reviews.all()

        context['review_form'] = ReviewForm()

        related_films = Film.objects.filter(
            actors__in=film.actors.all()
        ).exclude(
            pk=film.pk
        ).distinct()

        context['related_films'] = related_films

        return context

class FilmCreateView(CreateView):
    model = Film
    form_class = FilmForm
    template_name = 'films/film_form.html'
    success_url = reverse_lazy('film_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FilmUpdateView(UpdateView):
    model = Film
    form_class = FilmForm
    template_name = 'films/film_form.html'
    success_url = reverse_lazy('film_list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class FilmDeleteView(DeleteView):
    model = Film
    template_name = 'films/film_confirm_delete.html'
    success_url = reverse_lazy('film_list')

def add_review(request, pk):

    film = get_object_or_404(
        Film,
        pk=pk
    )

    if request.method == 'POST':

        form = ReviewForm(
            request.POST
        )

        if form.is_valid():

            review = form.save(
                commit=False
            )

            review.film = film
            review.user = request.user

            review.save()

    return redirect(
        'film_detail',
        pk=pk
    )    
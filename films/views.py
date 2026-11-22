from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .models import Film
from .forms import FilmForm


class FilmListView(ListView):
    model = Film
    template_name = 'films/film_list.html'
    context_object_name = 'films'
    paginate_by = 10


class FilmDetailView(DetailView):
    model = Film
    template_name = 'films/film_detail.html'


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
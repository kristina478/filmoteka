from django import forms
from .models import Film
from .models import Review

class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = [
            'title',
            'description',
            'release_year',
            'status',
            'genre',
            'actors',
        ]

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = [
            'text',
            'rating'
        ]
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.core.cache import cache

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Actor(models.Model):
    full_name = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name

class Film(models.Model):

    STATUS_CHOICES = (
        ('published', 'Published'),
        ('draft', 'Draft'),
    )

    title = models.CharField(
        max_length=255,
        verbose_name='Название'
    )

    description = models.TextField(
        verbose_name='Описание'
    )

    release_year = models.PositiveIntegerField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='published'
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='films'
    )

    actors = models.ManyToManyField(
        Actor,
        related_name='films'
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def average_rating(self):

        cache_key = f'film_rating_{self.id}'

        rating = cache.get(cache_key)

        if rating is None:

            rating = self.reviews.aggregate(
                Avg("rating")
            )["rating__avg"]

            cache.set(
                cache_key,
                rating,
                300
            )

        return rating

    def __str__(self):
        return self.title

class Review(models.Model):

    film = models.ForeignKey(
        Film,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user} - {self.film}'
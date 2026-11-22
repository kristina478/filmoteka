from django.contrib import admin
from .models import Film, Genre, Actor, Review


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'genre',
        'status',
        'author',
    )

    list_filter = (
        'genre',
        'status',
    )

    search_fields = (
        'title',
    )


admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Review)
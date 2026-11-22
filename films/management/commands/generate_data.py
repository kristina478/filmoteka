from django.core.management.base import BaseCommand
from faker import Faker
from films.models import Film, Genre, Actor
from django.contrib.auth.models import User
import random

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        fake = Faker('ru_RU')

        user, _ = User.objects.get_or_create(
            username='admin'
        )

        genres = []

        for i in range(20):

            genre = Genre.objects.create(
                name=f'Genre {i}'
            )

            genres.append(genre)

        actors = []

        for i in range(100):

            actor = Actor.objects.create(
                full_name=fake.name()
            )

            actors.append(actor)

        films = []

        for i in range(100000):

            film = Film.objects.create(
                title=fake.sentence(),
                description=fake.text(),
                release_year=random.randint(
                    1950,
                    2025
                ),
                status='published',
                genre=random.choice(
                    genres
                ),
                author=user
            )

            film.actors.add(
                random.choice(
                    actors
                )
            )

            films.append(film)

            if i % 1000 == 0:
                print(i)
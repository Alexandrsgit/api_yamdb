from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Title, Review, User)


FILE_MODEL = {
    'static/data/category.csv':
        {Category: ('id', 'name', 'slug')},
    'static/data/genre.csv':
        {Genre: ('id', 'name', 'slug')},
    'static/data/titles.csv':
        {Title: ('id', 'name', 'year', 'category_id')},
    'static/data/genre_title.csv':
        {GenreTitle: ('id', 'title_id', 'genre_id')},
    'static/data/users.csv':
        {User: ('id', 'username', 'email', 'role',
                'bio', 'first_name', 'last_name')},
    'static/data/review.csv':
        {Review: ('id', 'title_id', 'text', 'author_id', 'score', 'pub_date')},
    'static/data/comments.csv':
        {Comment: ('id', 'review_id', 'text', 'author_id', 'pub_date')}
}


class Command(BaseCommand):
    """Загрузка базы данных из csv файла."""

    def handle(self, *args, **options):
        for file, dictionary in FILE_MODEL.items():
            for model, fieldnames in dictionary.items():
                with open(file, newline='') as csvfile:
                    fields = DictReader(csvfile, fieldnames=fieldnames)
                    next(fields)
                    record = []
                    for row in fields:
                        records = model(**row)
                        record.append(records)
                if model.objects.exists():
                    model.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f'Данные модели {model} удалены!'))
                model.objects.bulk_create(record)
                self.stdout.write(self.style.SUCCESS(
                    f'Данные модели {model} загружены!))'))

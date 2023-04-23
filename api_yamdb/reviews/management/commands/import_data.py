from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import (Category, Comment, Genre, GenreTitle,
                            Title, Review, User)

MODEL_FILE = [
    (Category, 'static/data/category.csv'),
    (Genre, 'static/data/genre.csv'),
    (Title, 'static/data/titles.csv'),
    (GenreTitle, 'static/data/genre_title.csv'),
    (User, 'static/data/users.csv'),
    (Review, 'static/data/review.csv'),
    (Comment, 'static/data/comments.csv')
]


class Command(BaseCommand):
    """Загрузка базы данных из csv файла."""

    def handle(self, *args, **options):
        for model, fils in MODEL_FILE:
            with open(fils, newline='') as csvfile:
                record = []
                for row in DictReader(csvfile):
                    if model == Category or model == Genre:
                        records = model(**row)
                    if model == Title:
                        records = Title(id=row['id'], name=row['name'],
                                        year=row['year'],
                                        category_id=row['category'])
                    if model == GenreTitle:
                        records = GenreTitle(id=row['id'],
                                             genre_id=row['genre_id'],
                                             title_id=row['title_id'])
                    if model == User:
                        records = User(id=row['id'], username=row['username'],
                                       email=row['email'], role=row['role'])
                    if model == Review:
                        records = Review(id=row['id'],
                                         title_id=row['title_id'],
                                         text=row['text'],
                                         author_id=row['author'],
                                         score=row['score'],
                                         pub_date=row['pub_date'])
                    if model == Comment:
                        records = Comment(id=row['id'],
                                          review_id=row['review_id'],
                                          text=row['text'],
                                          author_id=row['author'],
                                          pub_date=row['pub_date'])
                    record.append(records)
                if model.objects.exists():
                    model.objects.all().delete()
                    self.stdout.write(self.style.SUCCESS(
                        f'Данные модели {model} удалены!'))
                model.objects.bulk_create(record)
                self.stdout.write(self.style.SUCCESS(
                    f'Данные модели {model} загружены!))'))

from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Category, Genre, GenreTitle, Title


class Command(BaseCommand):
    def handle(self, *args, **options):

        record = []
        for row in DictReader(open('static/data/category.csv')):
            records = Category(**row)
            # records=Category(id=row['id'], name=row['name'],
            #                  slug=row['slug'])
            record.append(records)
        Category.objects.all().delete()
        Category.objects.bulk_create(record)

        record = []
        for row in DictReader(open('static/data/genre.csv')):
            records = Genre(**row)
            # records=Genre(id=row['id'], name=row['name'], slug=row['slug'])
            record.append(records)
        Genre.objects.all().delete()
        Genre.objects.bulk_create(record)

        record = []
        for row in DictReader(open('static/data/titles.csv')):
            records = Title(id=row['id'], name=row['name'],
                            year=row['year'], category_id=row['category'])
            record.append(records)
        Title.objects.all().delete()
        Title.objects.bulk_create(record)

        record = []
        for row in DictReader(open('static/data/genre_title.csv')):
            records = GenreTitle(id=row['id'], title_id=row['title_id'],
                                 genre_id=row['genre_id'])
            record.append(records)
        GenreTitle.objects.all().delete()
        GenreTitle.objects.bulk_create(record)

        # record = []
        # for row in DictReader(open('static/data/users.csv')):
        #     records = User(
        #         id=row['id'], username=row['username'],
        #         email=row['email'], role=row['role'])
        #     record.append(records)
        # User.objects.all().delete()
        # User.objects.bulk_create(record)

        # record = []
        # for row in DictReader(open('static/data/review.csv')):
        #     records = Review(
        #         id=row['id'], title_id=row['title_id'],
        #         text=row['text'], author_id=row['author'],
        #         score=row['score'], pub_date=row['pub_date'])
        #     record.append(records)
        # Review.objects.all().delete()
        # Review.objects.bulk_create(record)

        # record = []
        # for row in DictReader(open('static/data/comments.csv')):
        #     records = Comment(
        #         id=row['id'], review_id=row['review_id'],
        #         text=row['text'], author_id=row['author'],
        #         pub_date=row['pub_date'])
        #     record.append(records)
        # Comment.objects.all().delete()
        # Comment.objects.bulk_create(record)

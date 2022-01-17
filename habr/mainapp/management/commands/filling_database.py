import random
import os
import requests

from mimesis import Text, BinaryFile, Person, Datetime
from mimesis import Internet

from django.core.management.base import BaseCommand
from django.core.files import File

from mainapp.models import ArticleCategories, Article, ArticleLike, ArticleComment
from authapp.models import User

# from mainapp.models import Article, ArticleLike, ArticleComment
from authapp.models import UserProfile


class Command(BaseCommand):
    help = 'Create Categories article, Articles, Likes and Comments'

    def handle(self, *args, **options):
        # GENERATE PROJECTS
        text = Text('ru')
        img_cls = BinaryFile()

        # CREATE USERS
        person = Person()
        birthday = Datetime()

        print('Заполняю таблицу USERS')

        for _ in range(30):
            username = person.username(mask='C')
            user = UserProfile(
                first_name=person.first_name(gender=None),
                last_name=person.last_name(gender=None),
                username=username,
                # email=person.email(domains=None, unique=True),
                # password=person.password(length=8),
                birthday=birthday.formatted_datetime(fmt="%Y-%m-%d"))

            img_url = Internet().stock_image(width=100, height=100, keywords=['люди'])

            img_file = requests.get(img_url)

            file_name = f'{username}.png'
            with open(file_name, 'wb') as file:
                file.write(img_file.content)

            with open(file_name, 'rb') as file:
                data = File(file)
                user.avatar.save(file_name, data, True)

            os.remove(file_name)
            user.save()

        # CREATE ARTICLE CATEGORIES
        ARTICLE_CATEGORIES = ['Дизайн', 'Веб-разработка', 'Мобильная разработка', 'Маркетинг']

        print('Заполняю таблицу ARTICLE CATEGORIES')
        for categories in ARTICLE_CATEGORIES:
            new_categories = ArticleCategories(name=categories)
            new_categories.save()

        # CREATE ARTICLES
        print('Заполняю таблицу ARTICLES')
        for i in range(30):
            # create article
            new_article = Article(
                title=text.title(),
                subtitle=text.sentence(),
                text=text.text(quantity=15))
            # set categories
            new_article.categories = random.choice(ArticleCategories.objects.all())
            # set author
            new_article.user = random.choice(UserProfile.objects.all())

            # create and set article images
            # TODO указать размер картинки для статей
            img_url = Internet().stock_image(width=1920, height=1080, keywords=['природа'])
            img_file = requests.get(img_url)

            file_name = f'{text.word()}.png'
            with open(file_name, 'wb') as file:
                file.write(img_file.content)

            with open(file_name, 'rb') as file:
                data = File(file)
                new_article.main_img.save(file_name, data, True)

            os.remove(file_name)

            # save article
            new_article.save()

        # CREATE LIKES
        print('Заполняю таблицу LIKES')
        for item in UserProfile.objects.all():
            new_like = ArticleLike(like=True)  # вот здесь указывает на ошибку лишнего аргумента
            new_like.article_like = random.choice(Article.objects.all())
            new_like.user = item
            new_like.save()

        # CREATE COMMENTS
        print('Заполняю таблицу COMMENTS')
        for item in UserProfile.objects.all():
            new_comment = ArticleComment(text=text.text(quantity=2))
            new_comment.article_comment = random.choice(Article.objects.all())
            new_comment.user = item
            new_comment.save()

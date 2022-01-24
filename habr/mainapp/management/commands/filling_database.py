import random
import os
import requests

from mimesis import Text, BinaryFile, Person, Datetime
from mimesis import Internet

from django.core.management.base import BaseCommand
from django.core.files import File

from mainapp.models import ArticleCategories, Article, ArticleLike, ArticleComment
from authapp.models import User

from mainapp.models import Article, ArticleLike, ArticleComment
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
        for _ in range(10):
            user = User(
                username=person.username(mask='C'),
                email=person.email(domains=None, unique=True),
                password=person.password(length=8))

            user.save()

        print('Заполняю таблицу USERS PROFILE')
        for item in User.objects.all():
            name = person.name()
            user_profile = UserProfile(
                user = item,
                name = name,
                birthday = birthday.formatted_datetime(fmt="%Y-%m-%d"),
                bio = " ".join([text.word() for i in range(0, 5)]))


            img_url = Internet().stock_image(width=50, height=50, keywords=['лицо'])
            img_file = requests.get(img_url)

            file_name = f'{name}.png'
            with open(file_name, 'wb') as file:
                file.write(img_file.content)

            with open(file_name, 'rb') as file:
                data = File(file)
                user_profile.avatar.save(file_name, data, True)

            os.remove(file_name)
            user_profile.save()


        # CREATE ARTICLE CATEGORIES
        ARTICLE_CATEGORIES = ['Дизайн', 'Веб-разработка', 'Мобильная разработка', 'Маркетинг']

        print('Заполняю таблицу ARTICLE CATEGORIES')
        for categories in ARTICLE_CATEGORIES:
            new_categories = ArticleCategories(name=categories)
            new_categories.save()

        # CREATE ARTICLES
        print('Заполняю таблицу ARTICLES')
        for i in range(10):
            # create article
            new_article = Article(
                title=" ".join([text.word() for i in range(0, 5)]),
                subtitle=" ".join([text.word() for i in range(0, 10)]),
                text=text.text(quantity=15))
            # set categories
            new_article.categories = random.choice(ArticleCategories.objects.all())
            # set author
            new_article.user = random.choice(User.objects.all())

            # create and set article images
            img_url = Internet().stock_image(width=390, height=300, keywords=['природа'])
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
        for item in User.objects.all():
            new_like = ArticleLike(like=True)
            new_like.article_like = random.choice(Article.objects.all())
            new_like.user = item
            new_like.save()

        # CREATE COMMENTS
        print('Заполняю таблицу COMMENTS')
        for item in User.objects.all():
            count = random.choice([i for i in range(0,10)])
            for i in range(0, count):
                new_comment = ArticleComment(text=text.text(quantity=2))
                new_comment.article_comment = random.choice(Article.objects.all())
                new_comment.user = item
                new_comment.save()
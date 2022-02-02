import random
import os
import requests

from mimesis import Text, BinaryFile, Person, Datetime
from mimesis import Internet

from django.core.management.base import BaseCommand
from django.core.files import File

from mainapp.models import ArticleCategories
from authapp.models import User

from mainapp.models import Article, ArticleComment
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
                user=item,
                name=name,
                birthday=birthday.formatted_datetime(fmt="%Y-%m-%d"),
                bio="Этот автор - самый крутой. Статьи у него пушка-бомба!")

            img_url = Internet().stock_image(width=50, height=50, keywords=['лицо'])
            img_file = requests.get(img_url)

            file_name = f'{name}.png'
            with open(file_name, 'wb') as file:
                file.write(img_file.content)

            with open(file_name, 'rb') as file:
                data = File(file)
                user_profile.avatar.save(file_name, data, True)

            os.remove(file_name)
            # заполняется поле stars у таблицы USERS PROFILE
            for _ in range(random.randint(0, 10)):
                user_liked = random.choice(User.objects.all())
                if user_liked in user_profile.stars.all():
                    user_profile.stars.remove(user_liked)
                else:
                    user_profile.stars.add(user_liked)

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
            new_article = Article()
            # set categories
            new_article.categories = random.choice(ArticleCategories.objects.all())
            # set author
            new_article.user = random.choice(User.objects.all())
            new_article.title = f'Заголовок статьи #{i} автора {new_article.user.username}'
            new_article.subtitle = f'Падзаголовок статьи #{i} автора {new_article.user.username}'
            new_article.text = text.text(quantity=15)

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
            # заполняется поле likes у таблицы ARTICLES
            for _ in range(random.randint(0, 10)):
                user_liked = random.choice(User.objects.all())
                if user_liked in new_article.likes.all():
                    new_article.likes.remove(user_liked)
                else:
                    new_article.likes.add(user_liked)

            # save article
            new_article.save()

        # CREATE COMMENTS
        print('Заполняю таблицу COMMENTS')
        for item in User.objects.all():
            count = random.choice([i for i in range(0, 10)])
            for i in range(0, count):
                new_comment = ArticleComment(text=text.text(quantity=2))
                new_comment.article_comment = random.choice(Article.objects.all())
                new_comment.user = item
                new_comment.save()
                # заполняется поле likes у таблицы COMMENTS
                for _ in range(random.randint(0, 10)):
                    user_liked = random.choice(User.objects.all())
                    if user_liked in new_comment.likes.all():
                        new_comment.likes.remove(user_liked)
                    else:
                        new_comment.likes.add(user_liked)

import random
import os

from mimesis import Text, BinaryFile
from mimesis.enums import ImageFile
from django.core.management.base import BaseCommand
from django.core.files import File

from mainapp.models import Article, ArticleLike, ArticleComment
from authapp.models import User


class Command(BaseCommand):
    help = 'Create Articles, Likes and Comments'

    def handle(self, *args, **options):
        # GENERATE PROJECTS
        text = Text('ru')
        img_cls = BinaryFile()

        # CREATE USERS
        # TODO add create users in database

        # CREATE ARTICLES
        for i in range(20):
            # create article
            new_article = Article(article_title=text.title(),
                                  article_subtitle=text.title(),
                                  article_text=text.text(quantity=15))
            # set author
            new_article.user = random.choice(User.objects.all())

            # create and set article images
            file_name = f'{text.word()}.png'
            with open(file_name, 'wb') as file:
                file.write(img_cls.image(file_type=ImageFile.PNG))

            with open(file_name, 'rb') as file:
                data = File(file)
                new_article.article_main_img.save(file_name, data, True)

            os.remove(file_name)

            # save article
            new_article.save()

        # CREATE LIKES
        for item in Article.objects.all():
            new_like = ArticleLike(article_like=True)
            new_like.article_to_like = item
            new_like.user = random.choice(User.objects.all())
            new_like.save()

        # CREATE COMMENTS
        for item in Article.objects.all():
            new_comment = ArticleComment(comment_text=text.text(quantity=2))
            new_comment.article_to_comment = item
            new_comment.user = random.choice(User.objects.all())
            new_comment.save()

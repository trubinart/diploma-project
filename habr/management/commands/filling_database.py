import random
import os

from mimesis import Text, BinaryFile
from mimesis.enums import ImageFile
from django.core.management.base import BaseCommand
from django.core.files import File

from article.models import Article, ArticleLike, ArticleComment

class Command(BaseCommand):
    help = 'Create Articles, Likes and Comments'

    def handle(self, *args, **options):
        #GENERATE PROJECTS
        text = Text('ru')
        img_cls = BinaryFile()

        # CREATE USERS
        #TODO add create users in database

        #CREATE ARTICLES
        for i in range(1):
            new_article = Article(article_title = text.title(),
                                  article_subtitle = text.title(),
                                  article_text = text.text(quantity=15))

            file_name = f'{text.word()}.png'
            with open(file_name, 'wb') as file:
                file.write(img_cls.image(file_type=ImageFile.PNG))

            with open(file_name, 'rb') as file:
                data = File(file)
                new_article.article_main_img.save(file_name, data, True)

            os.remove(file_name)
            new_article.save()

        # CREATE LIKES
        # TODO add users in likes
        for item in Article.objects.all():
            new_like = ArticleLike(article_like=True)
            new_like.article_to_like = item
            new_like.save()

      # CREATE COMMENTS
        # TODO add users in comments
        for item in Article.objects.all():
            new_comment = ArticleComment(comment_text = text.text(quantity=2))
            new_comment.article_to_comment = item
            new_comment.save()

# if __name__ == "__main__":
#     img = BinaryFile()
#     msg = img.image(file_type=ImageFile.PNG)
#     msg_2 = img.image(file_type=ImageFile.PNG)
#     with open('12356.png', 'wb') as file:
#         file.write(msg_2)


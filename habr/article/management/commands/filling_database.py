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


# if __name__ == "__main__":
#     img = BinaryFile()
#     msg = img.image(file_type=ImageFile.PNG)
#     msg_2 = img.image(file_type=ImageFile.PNG)
#     with open('12356.png', 'wb') as file:
#         file.write(msg_2)


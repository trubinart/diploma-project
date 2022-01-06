import random

from mimesis import Text
from django.core.management.base import BaseCommand

from habr.article.models import Article, ArticleLike, ArticleComment

text = Text('ru')

class Command(BaseCommand):
    help = 'Create Articles, Likes and Comments'

    def handle(self, *args, **options):
        #GENERATE PROJECTS
        pass
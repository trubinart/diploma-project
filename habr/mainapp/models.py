import uuid
import datetime
from time import sleep

from django.db import models
from django.db.models.query import QuerySet
from django.core.paginator import Paginator

from authapp.models import User


class BaseModel(models.Model):
    """
    Global model. Set id and created_timestamp for all children models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')

    @classmethod
    def get_item_by_id(cls, search_id):
        return cls.objects.filter(id=search_id)


class ArticleCategories(BaseModel):
    """
    Models for Article Categories
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='name categories')
    is_active = models.BooleanField(default=True, verbose_name='active')

    def __str__(self):
        return self.name


# function for creating a unique article number
def uniq_number_article():
    gen_number = datetime.datetime.today().strftime("%d%m%H%M%S%f")[:-4]
    sleep(0.1)
    return gen_number


class Article(BaseModel):
    """
    Models for Articles
    """
    article_number = models.PositiveIntegerField(default=uniq_number_article, unique=True,
                                                 verbose_name='article number')
    categories = models.ForeignKey(ArticleCategories, on_delete=models.CASCADE, verbose_name='categories')
    title = models.CharField(max_length=60, verbose_name='title')
    subtitle = models.CharField(max_length=100, verbose_name='subtitle')
    main_img = models.ImageField(upload_to='article_images', verbose_name='img')
    text = models.TextField(max_length=5000, verbose_name='Text Article')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author article',
                             related_name='article_author')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'article'
        ordering = ['-created_timestamp']

    @classmethod
    def get_all_articles(cls) -> QuerySet:
        """
        :param: None
        :return: QuerySet with all Articles in DataBase

        Method for get QuerySet with all ARTICLES in DataBase.
        Method called from Classes.
        All article sorted by date descending order.
        """
        return Article.objects.all()

    @classmethod
    def get_all_articles_in_pagination(cls, pagination_page: int) -> Paginator:
        """
        :param: desired count page in pagination
        :return: QuerySet with all ARTICLES in DataBase in Pagination object

          Method called from Classes.
          All article sorted by date descending order.
          """
        all_articles: QuerySet = cls.get_all_articles()
        pagination_articles: Paginator = Paginator(all_articles, pagination_page)
        return pagination_articles

    def get_likes_by_article_id(self) -> QuerySet:
        """
        :param: None
        :return: QuerySet with all LIKES in DataBase by specific Article.

          Method called from Article Item.
          All likes sorted by date descending order.
          """
        return ArticleLike.objects.select_related('article_like').filter(article_like=self.id)

    def get_comments_by_article_id(self) -> QuerySet:
        """
        :param: None
        :return: QuerySet with all COMMENTS in DataBase by specific Article.

          Method called from Article Item.
          All likes sorted by date descending order.
          """
        return ArticleComment.objects.select_related('article_comment').filter(article_like=self.id)


class ArticleLike(BaseModel):
    """
    Models for Articles Likes
    """
    like = models.BooleanField(verbose_name='Like')
    article_like = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='Article for like',
                                     related_name='article_like')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Like Author',
                                related_name='like_author')

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'article_likes'
        ordering = ['-created_timestamp']


class ArticleComment(BaseModel):
    """
    Models for Articles Comments
    """
    article_comment = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='Article for comment',
                                        related_name='article_comment')
    text = models.TextField(max_length=300, verbose_name='Comment text')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Comment Author',
                                related_name='comment_author')

    def __str__(self):
        return self.article_comment.user.username

    class Meta:
        db_table = 'article_comments'
        ordering = ['-created_timestamp']

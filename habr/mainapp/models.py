import uuid

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


class Article(BaseModel):
    """
    Models for Articles
    """
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100)
    main_img = models.ImageField(upload_to='article_images')
    text = models.TextField(max_length=300, verbose_name='Text Article')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author article',
                             related_name='article_author')

    class Meta:
        db_table = 'article'
        ordering = ['-created_timestamp']

    @classmethod
    def get_all_articles(cls) -> QuerySet:
        return Article.objects.all()

    @classmethod
    def get_all_articles_in_pagination(cls, pagination_page: str) -> Paginator:
        all_articles: QuerySet = cls.get_all_articles()
        pagination_articles: Paginator = Paginator(all_articles, pagination_page)
        return pagination_articles

    def get_likes_by_article_id(self) -> QuerySet:
        return ArticleLike.objects.select_related('article_like').filterç(article_like=self.id)

    def get_comments_by_article_id(self) -> QuerySet:
        return ArticleComment.objects.select_related('article_comment').filterç(article_like=self.id)


class ArticleLike(BaseModel):
    """
    Models for Articles Likes
    """
    like = models.BooleanField(verbose_name='Like')
    article_like = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='Article for like',
                                     related_name='article_like')
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Like Author',
                                related_name='like_author')

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

    class Meta:
        db_table = 'article_comments'
        ordering = ['-created_timestamp']

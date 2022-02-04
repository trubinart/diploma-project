import uuid
import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.urls import reverse
from django.db.models.signals import m2m_changed, post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg

from authapp.models import User, UserProfile
from mainapp.manager import ArticleManager


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


class Article(BaseModel):
    """
    Models for Articles
    """
    # добавили менеджер для изменения логики поиска в модели
    objects = ArticleManager()

    categories = models.ForeignKey(ArticleCategories, on_delete=models.CASCADE, verbose_name='categories')
    title = models.CharField(max_length=60, verbose_name='title')
    subtitle = models.CharField(max_length=100, verbose_name='subtitle')
    main_img = models.ImageField(upload_to='article_images', verbose_name='img')
    text = RichTextUploadingField(config_name='awesome_ckeditor')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Author article',
                             related_name='article_author')
    likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
    rating = models.PositiveIntegerField(default=0, verbose_name='article_rating')

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

    def get_comment_count_by_article_id(self) -> int:
        """
        Подсчет количества комментариев для статьи.
        """
        return ArticleComment.objects.select_related('article_comment').filter(article_comment=self.id).count()

    def get_comments_by_article_id(self) -> QuerySet:
        """
        :param: None
        :return: QuerySet with all COMMENTS in DataBase by specific Article.

          Method called from Article Item.
          All likes sorted by date descending order.
          """
        return ArticleComment.objects.select_related('article_comment').filter(article_comment=self.id)

    def get_other_articles_by_author(self) -> QuerySet:
        """
        Метод выводит последние по дате 3 статьи автора исключая текущую статью
          """
        return Article.objects.filter(user=self.user).exclude(id=self.id).order_by('-created_timestamp')[:3]

    def get_absolute_url(self):
        """
        Метод отдает абсолютную ссылку на страницу статьи
        """
        return reverse("article", kwargs={"pk": self.id})

    def get_article_text_preview(self):
        """
        Метод выводит первые 250 символов текста статьи
        """
        preview = re.sub(r'\<[^>]*\>', '', self.text)
        return f'{preview[:250]}.....'

    def get_like_url(self):
        """
        Метод отдает ссылку по которой статья получает лайк
        """
        return reverse("like-toggle", kwargs={"pk": self.id})

    def get_like_api_url(self):
        """
        Метод отдает ссылку для перехода в api rest_framework
        """
        return reverse("like-api-toggle", kwargs={"pk": self.id})


class ArticleComment(BaseModel):
    """
    Models for Articles Comments
    """
    article_comment = models.ForeignKey(Article, on_delete=models.DO_NOTHING, verbose_name='Article for comment',
                                        related_name='article_comment')
    text = models.TextField(max_length=300, verbose_name='Comment text')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Comment Author',
                             related_name='comment_author')
    likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')

    def __str__(self):
        return f'from "{self.user.username}" for "{self.article_comment.title}"'

    class Meta:
        db_table = 'article_comments'
        ordering = ['-created_timestamp']


@receiver(m2m_changed, sender=ArticleComment.likes.through)
def change_author_rating_by_likes_to_author_comments(sender, instance, action, **kwargs):
    """
    Сигнал для изменения рейтинга автора от изменения лайков к комментариям этого автора
    """

    author = UserProfile.objects.get(user=instance.user.id)

    if action == 'post_add':
        author.rating += 1
        author.save()

    if action == 'post_remove' and author.rating != 0:
        author.rating -= 1
        author.save()

    elif action == 'post_remove' and author.rating == 0:
        author.rating = 0
        author.save()


@receiver(post_save, sender=Article)
@receiver(post_delete, sender=Article)
def change_author_rating_by_article_rating(sender, instance, **kwargs):
    """
    Сигнал для изменения рейтинга автора от изменения рейтинга статей этого автора
    """
    author = instance.user.userprofile
    previous_article_rating = author.previous_article_rating
    author.rating -= previous_article_rating

    article_by_author = Article.objects.filter(user=instance.user)
    new_article_rating = article_by_author.aggregate(avg_duration=Avg('rating'))['avg_duration']
    author.rating += int(new_article_rating)
    author.previous_article_rating = int(new_article_rating)
    print(f'author.rating - {author.rating}')

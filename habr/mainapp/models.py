import uuid
import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver

from authapp.models import User
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


class ModeratorNotification(BaseModel):
    """
    Модель для хранения  и уведомления модератора о наличии жалобы на статью
    """

    NEW = 'N'
    ASSIGNED = 'A'
    UNDER_CONSIDERATION = 'U'
    REVIEWED = 'R'

    STATUS_CHOICES = (
        (NEW, 'Новая'),
        (ASSIGNED, 'Назначена'),
        (UNDER_CONSIDERATION, 'На рассмотрении'),
        (REVIEWED, 'Рассмотрена'),
    )

    comment_initiator = models.ForeignKey(
        ArticleComment,
        on_delete=models.DO_NOTHING,
        verbose_name='Comment initiator',
        related_name='comment_initiator'
    )
    responsible_moderator = models.OneToOneField(
        User,
        on_delete=models.DO_NOTHING,
        verbose_name='Responsible moderator',
        related_name='responsible_moderator',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        verbose_name='Статус',
        default='N'
    )

    def __str__(self):
        return f'Запрос на проверку статьи "{self.comment_initiator.article_comment}" ' \
               f'от "{self.comment_initiator.user}"'

    class Meta:
        db_table = 'moderator_notification'
        ordering = ['-created_timestamp']

    @staticmethod
    def get_count_new_requests_moderation():
        return ModeratorNotification.objects.filter(status='N').count()

    @receiver(post_save, sender=ArticleComment)
    def create_moderator_notification(sender, instance, **kwargs):
        if '@moderator' in instance.text:
            ModeratorNotification.objects.create(comment_initiator=instance,)




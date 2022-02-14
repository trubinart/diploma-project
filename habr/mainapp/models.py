import uuid
import re

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.db.models.signals import post_save
from django.urls import reverse

from django.dispatch import receiver

from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from django.db.models import Avg
from taggit.managers import TaggableManager
from taggit.models import GenericUUIDTaggedItemBase, TaggedItemBase, Tag

from authapp.models import User, UserProfile
from mainapp.manager import ArticleManager


class UUIDTaggedItem(GenericUUIDTaggedItemBase, TaggedItemBase):
    tag = models.ForeignKey(Tag, related_name="uuid_tagged_items", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"


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
    tags = TaggableManager(through=UUIDTaggedItem)

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

    def get_rating_by_article_id(self) -> QuerySet:
        """
        Получение рейтинга для статьи.
        """
        # return ArticleRating.objects.filter(article_rating=self.id).select_related('rating')
        return ArticleRating.objects.get(article_rating=self.id).rating


# сигнал для создания таблицы рейтинга к статье
@receiver(post_save, sender=Article)
def create_article_rating(instance, created, **kwargs):
    if created:
        new_rating = ArticleRating()
        new_rating.article_rating = instance
        new_rating.article_author = instance.user
        new_rating.save()
        return None


class ArticleComment(BaseModel):
    """
    Models for Articles Comments
    """
    article_comment = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Article for comment',
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
    responsible_moderator = models.ForeignKey(
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
        status_verbose_names = {'N': 'Новая',
                                'A': 'Назначена',
                                'U': 'На рассмотрении',
                                'R': 'Рассмотрена'}
        return f'Запрос на проверку статьи "{self.comment_initiator.article_comment}"; ' \
               f'от "{self.comment_initiator.user}"; ' \
               f'статус заявки: {status_verbose_names[self.status]}.'

    class Meta:
        db_table = 'moderator_notification'
        ordering = ['-created_timestamp']

    @staticmethod
    def get_count_new_requests_moderation():
        return ModeratorNotification.objects.filter(status='N').count()

    @receiver(post_save, sender=ArticleComment)
    def create_moderator_notification(sender, instance, **kwargs):
        if '@moderator' in instance.text:
            ModeratorNotification.objects.create(comment_initiator=instance, )


class ArticleRating(BaseModel):
    """
    Models for Articles Rating
    """
    article_rating = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='article_for_rating',
                                       related_name='article_rating')
    rating = models.PositiveSmallIntegerField(default=0, verbose_name='rating')
    article_author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='article_author')

    def __str__(self):
        return f'from article "{self.article_rating.title}" rating = "{self.rating}"'

    class Meta:
        db_table = 'article_rating'
        ordering = ['rating']


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


@receiver(post_save, sender=ArticleRating)
@receiver(post_delete, sender=ArticleRating)
def change_author_rating_by_article_rating(sender, instance, **kwargs):
    """
    Сигнал для изменения рейтинга автора от изменения рейтинга статей этого автора
    """
    author = instance.article_rating.user
    instance.article_author = author

    previous_article_rating = author.userprofile.previous_article_rating
    author.userprofile.rating -= previous_article_rating

    rating_objects_by_author = None if not ArticleRating.objects.filter(article_author=author) \
        else ArticleRating.objects.filter(article_author=author)

    if not rating_objects_by_author:
        new_article_rating = instance.rating
    else:
        new_article_rating = rating_objects_by_author.aggregate(avg_duration=Avg('rating'))['avg_duration']

    author.userprofile.rating += int(new_article_rating)
    author.userprofile.previous_article_rating = int(new_article_rating)

    author.save()


@receiver(m2m_changed, sender=Article.likes.through)
def change_article_rating_by_likes_to_article(instance, action, **kwargs):
    """
    Сигнал для изменения рейтинга статьи от изменения кол-ва лайков к статье
    """
    article_rating = ArticleRating.objects.get(article_rating_id=instance.id)
    # ценость одного лайка и одного комментария
    value_one_like = 1
    value_one_comments = 0.2
    if action in ['post_add', 'post_remove']:
        new_article_rating = instance.likes.count() * value_one_like + int(
            instance.get_comment_count_by_article_id() * value_one_comments)
        article_rating.rating = new_article_rating
        article_rating.save()
        return None


@receiver(post_save, sender=ArticleComment)
def change_article_rating_by_count_comments_to_article(instance, **kwargs):
    """
    Сигнал для изменения рейтинга статьи от изменения кол-ва комментов к статье
    """
    article_rating = ArticleRating.objects.get(article_rating_id=instance.article_comment.id)
    # ценость одного лайка и одного комментария
    value_one_like = 1
    value_one_comments = 0.2
    new_article_rating = instance.article_comment.likes.count() * value_one_like + int(
        instance.article_comment.get_comment_count_by_article_id() * value_one_comments)
    article_rating.rating = new_article_rating
    article_rating.save()
    return None

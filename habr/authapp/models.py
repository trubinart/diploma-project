import inspect
import uuid
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.signals import request_finished, got_request_exception, request_started
from django.db import models
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

import mainapp.models as mainapp_models


class BaseModel(models.Model):
    """
    Global model. Set id and created_timestamp for all children models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')

    @classmethod
    def get_item_by_id(cls, search_id):
        return cls.objects.filter(id=search_id)


class User(AbstractUser, BaseModel, PermissionsMixin):
    """
    Model for user`s registration
    """
    username = models.CharField(verbose_name='user_name', unique=True, max_length=25, blank=False)
    email = models.EmailField(verbose_name='email', unique=True, blank=False)
    password = models.CharField(verbose_name='password', max_length=250, blank=False)
    first_name = None
    last_name = None
    is_banned = models.BooleanField(default=False, verbose_name='Заблокирован')
    date_end_banned = models.DateTimeField(null=True, blank=True, default=None)

    def __init__(self, *args, **kwargs):
        """ для фиксации изменений о статусе аккаунта"""
        super(User, self).__init__(*args, **kwargs)
        self.__original_is_banned = self.is_banned
        self.__original_date_end_banned = self.date_end_banned

    def __str__(self):
        return f"{self.username} - {self.userprofile.name}"

    def get_profile(self):
        """
        Метод отдает профиль текущего пользователя
        """
        return UserProfile.objects.filter(user=self).select_related("user").first()

    def get_absolute_url(self):
        """
        Метод отдает абсолютную ссылку на страницу статей автора
        """
        return reverse("user_article", kwargs={"pk": self.id})

    def get_count_notifications_on_moderation(self):
        return mainapp_models.ModeratorNotification.objects.filter(
            responsible_moderator=self
        ).exclude(
            status='R'
        ).count()

    @property
    def is_now_banned(self) -> bool:
        if self.is_banned:
            return True
        if self.date_end_banned and self.date_end_banned > timezone.now():
            return True
        return False

    def get_notification_about_blocking(self):
        return NotificationUsersAboutBlocking.objects.filter(
            blocked_user=self
        ).exclude(
            is_read=True
        ).select_related(
            "blocked_user"
        ).order_by(
            '-created_timestamp'
        )

    def get_count_notifications_about_blocking(self):
        return NotificationUsersAboutBlocking.objects.filter(
            blocked_user=self
        ).exclude(
            is_read=True
        ).select_related(
            "blocked_user"
        ).count()


class UserProfile(models.Model):
    """
    Model for users
    """
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя Фамилия', max_length=100, blank=False)
    birthday = models.DateField(verbose_name='День рождения', null=True, blank=True)
    bio = models.TextField(verbose_name='Краткое описание', max_length=120, blank=False)
    avatar = models.ImageField(verbose_name='Аватар', upload_to='user_avatars')
    stars = models.ManyToManyField(User, blank=True, related_name='author_stars')
    rating = models.PositiveIntegerField(default=0, verbose_name='author_rating')
    previous_article_rating = models.PositiveIntegerField(default=0, verbose_name='article_previous_rating')

    def __str__(self):
        return f'Userprofile for "{self.user.username}"'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, update_fields, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()


@receiver(m2m_changed, sender=UserProfile.stars.through)
def change_author_rating_by_author_likes(sender, instance, action, **kwargs):
    """
    Сигнал для изменения рейтинга автора от изменения лайков этому автору
    """
    if action == 'post_add':
        instance.rating += 1
        instance.save()

    if action == 'post_remove' and instance.rating != 0:
        instance.rating -= 1
        instance.save()


class NotificationUsersAboutBlocking(BaseModel):
    """
    Уведомление пользователей о блокировке
    """
    blocked_user = models.ForeignKey(
        User,
        null=False,
        db_index=True,
        on_delete=models.CASCADE,
        verbose_name='кто заблокирован'
    )

    moderator_who_blocked = models.UUIDField(
        verbose_name='кем заблокирован',
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name='прочитано',
    )

    message = models.CharField(
        max_length=350,
        verbose_name='дата снятия блокировки',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'уведомление о блокировке пользователя "{self.blocked_user.username}"'

    @staticmethod
    def get_moderator(inspect_stack):
        """получаем модератора из request"""
        for frame_record in inspect_stack:
            if frame_record[3] == 'get_response':
                request = frame_record[0].f_locals['request']
                return request.user
        return

    @staticmethod
    def get_full_message(part_1, part_2):
        """создаем строку сообщения"""
        if part_1 and part_2:
            return f'<p>{part_1}</p><p>{part_2}</p>'
        if part_1:
            return f'<p>{part_1}</p>'

    @receiver(post_save, sender=User)
    def create_moderator_notification(sender, instance, **kwargs):
        """
        При изменении модели User проверяем, изменились ли данные,
        отвечающие за блокировку пользователя. В зависимости от изменений,
        отправляем соответствующие сообщения, если требуется.
        Если изменений не было; если пользователь как был заблокирован
        бессрочно, так и остался; или пользователь как не был заблокирован,
        так и остался не заблокирован - уведомление не создается
        """
        #  получаем составные части сообщения
        part_1, part_2 = '', ''  # все сообщения будут формироваться из этих кусков
        if instance.is_banned != instance._User__original_is_banned:  # было изм. поле is_banned
            if instance.is_banned:  # уст. бессрочный бан
                part_1 = "Ваш аккаунт заблокирован модератором бессрочно."
            else:
                part_1 = "C Вашего аккаунта снята бессрочная блокировка."
                if instance.is_now_banned:  # в настоящий момент действует временный бан
                    part_2 = f'Ваш аккаунт заблокирован модератором до' \
                             f' {instance.date_end_banned.strftime("%d.%m.%Y %H:%M:%S %Z")}.'
        elif not instance.is_banned and \
                instance.date_end_banned != instance._User__original_date_end_banned:
            # было изменение временной блокировки, и нет бессрочного бана
            if instance.is_now_banned:  # временная блокировка действует
                part_1 = f'Ваш аккаунт заблокирован модератором ' \
                         f'до {str(instance.date_end_banned.strftime("%d.%m.%Y %H:%M:%S %Z"))}.'
            elif instance._User__original_date_end_banned \
                    and instance._User__original_date_end_banned > timezone.now():
                # действовал временный бан, но был снят
                part_1 = f'C Вашего аккаунта снята временная блокировка.'
            else:
                return  # если пользователь как не был заблокирован, так и остался не заблокирован
        else:
            return  # если ни чего не менялось или если пользователь как был заблокирован бессрочно, так и остался

        message = NotificationUsersAboutBlocking.get_full_message(part_1, part_2)
        moderator = NotificationUsersAboutBlocking.get_moderator(inspect.stack())

        NotificationUsersAboutBlocking.objects.create(
            blocked_user=instance,
            moderator_who_blocked=moderator.pk,
            message=message
        )

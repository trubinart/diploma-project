import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    """
    Global model. Set id and created_timestamp for all children models.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='id')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Create Date')

    @classmethod
    def get_item_by_id(cls, search_id):
        return cls.objects.filter(id=search_id)


class User(AbstractUser, BaseModel):
    """
    Model for user`s registration
    """
    username = models.CharField(verbose_name='user_name', unique=True, max_length=25, blank=False)
    email = models.EmailField(verbose_name='email', unique=True, blank=False)
    password = models.CharField(verbose_name='password', max_length=25, blank=False)

    def __str__(self):
        return self.username

    def get_profile(self):
        """
        Метод отдает профиль текущего пользователя
        """
        return UserProfile.objects.filter(user=self).select_related("user").first()


class UserProfile(models.Model):
    """
    Model for users
    """
    user = models.OneToOneField(User, unique=True, null=False, db_index=True, on_delete=models.CASCADE)
    birthday = models.DateField(verbose_name='birthday', null=True, blank=True)
    bio = models.TextField(verbose_name='description', max_length=250, blank=False)
    avatar = models.ImageField(upload_to='user_avatars')

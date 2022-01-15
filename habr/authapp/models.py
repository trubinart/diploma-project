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
    Model for users
    """
    first_name = models.CharField(verbose_name='first_name', max_length=25, blank=True)
    last_name = models.CharField(verbose_name='last_name', max_length=25, blank=True)
    username = models.CharField(verbose_name='user_name', unique=True, max_length=25, blank=True)
    email = models.EmailField(verbose_name='email', unique=True, blank=True)
    password = models.CharField(verbose_name='password', max_length=25, blank=True)
    birthday = models.DateField(verbose_name='birthday', null=True, blank=True)
    avatar = models.ImageField(upload_to='user_avatars')
    date_joined = False

    def __str__(self):
        return self.username

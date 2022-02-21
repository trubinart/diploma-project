from django.contrib import admin

from authapp.models import User, UserProfile
from mainapp.models import NotificationUsersFromModerator

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(NotificationUsersFromModerator)

from django.contrib import admin

from authapp.models import User, UserProfile, NotificationUsersAboutBlocking

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(NotificationUsersAboutBlocking)

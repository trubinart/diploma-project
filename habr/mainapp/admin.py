from django.contrib import admin

from mainapp.models import ArticleCategories, Article, ArticleComment, ModeratorNotification

admin.site.register(ArticleCategories)
admin.site.register(Article)
# admin.site.register(ArticleLike)
admin.site.register(ArticleComment)
admin.site.register(ModeratorNotification)


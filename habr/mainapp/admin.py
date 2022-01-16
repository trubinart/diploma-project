from django.contrib import admin

from mainapp.models import Article, ArticleLike, ArticleComment, ArticleCategories

admin.site.register(Article)
admin.site.register(ArticleLike)
admin.site.register(ArticleComment)
admin.site.register(ArticleCategories)

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from mainapp.views import MainListView, LkListView, ArticleDetailView, \
    CategoriesListView, UserArticleListView, CreateCommentView, \
    CreateArticle, UpdateArticle

from authapp.views import UserRegistrationView

urlpatterns = [

    path('', MainListView.as_view(), name='main'),
    path('lk/', LkListView.as_view(), name='lk'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('article-add/', CreateArticle.as_view(), name='article_create'),
    path('article-update/<str:pk>/', UpdateArticle.as_view(), name='article_update'),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('add-comment/', CreateCommentView.as_view(), name='add-comment'),
    path('category/<str:pk>/', CategoriesListView.as_view(), name='category'),
    path('user-article/<str:pk>/', UserArticleListView.as_view(), name='user_article'),
    path('auth/', include('authapp.urls', namespace='auth')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import never_cache

from mainapp.views import MainListView, LkListView, ArticleDetailView, \
    CategoriesListView, UserArticleListView, CreateCommentView, CreateArticle, SearchView, \
    ArticleLikeRedirectView, ArticleLikeRedirectAPIView, CommentLikeRedirectView, AuthorArticleStarRedirectView

from mainapp.views import AuthorStarRedirectView
from ckeditor_uploader import views

urlpatterns = [

    path('', MainListView.as_view(), name='main'),
    path('lk/', LkListView.as_view(), name='lk'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('article-add/', CreateArticle.as_view(), name='article_create'),
    path('add-comment/', CreateCommentView.as_view(), name='add-comment'),
    path('category/<str:pk>/', CategoriesListView.as_view(), name='category'),
    path('user-article/<str:pk>/', UserArticleListView.as_view(), name='user_article'),
    path('auth/', include('authapp.urls', namespace='auth')),

    path('ckeditor/upload/', login_required(views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(views.browse)), name="ckeditor_browse"),

    path('search/', SearchView.as_view(), name='search'),
    path('admin/', admin.site.urls),

    path('article/<str:pk>/like/', ArticleLikeRedirectView.as_view(), name='like-toggle'),
    path('api/article/<str:pk>/like/', ArticleLikeRedirectAPIView.as_view(), name='like-api-toggle'),

    path('article/<str:pk>/star/', AuthorStarRedirectView.as_view(), name='star_toggle'),
    path('article/<str:pk>/like/<str:id>', CommentLikeRedirectView.as_view(), name='like_comment_toggle'),
    path('user-article/<str:pk>/star/', AuthorArticleStarRedirectView.as_view(), name='user_article_star_toggle'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

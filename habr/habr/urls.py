from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import MainListView, LkListView, ArticleDetailView, \
    CategoriesListView, UserArticleListView, CreateCommentView, SearchView
from authapp.views import UserRegistrationView

urlpatterns = [

    path('', MainListView.as_view(), name='main'),
    path('lk/', LkListView.as_view(), name='lk'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('add-comment/', CreateCommentView.as_view(), name='add-comment'),
    path('category/<str:pk>/', CategoriesListView.as_view(), name='category'),
    path('user-article/<str:pk>/', UserArticleListView.as_view(), name='user_article'),
    path('search/', SearchView.as_view(), name='search'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

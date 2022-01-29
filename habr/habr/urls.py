from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import MainListView, ArticleDetailView, \
    CategoriesListView, UserArticleListView, CreateCommentView, LkEditView, LkListView #UpdateView
from authapp.views import UserRegistrationView

urlpatterns = [

    path('', MainListView.as_view(), name='main'),
    # path('lk/', LkListView.as_view(), name='lk'),
    path('lk/', LkListView.as_view(), name='lk'),
    path('lk/edit/', LkEditView.as_view(), name='lk_edit'),
    # path('lk/<str:pk>/update/', LkUpdateView.as_view(), name='lk_update'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('add-comment/', CreateCommentView.as_view(), name='add-comment'),
    path('category/<str:pk>/', CategoriesListView.as_view(), name='category'),
    path('user-article/<str:pk>/', UserArticleListView.as_view(), name='user_article'),
    path('auth/', include('authapp.urls', namespace='auth')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

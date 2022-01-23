from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import MainListView, LkListView, ArticleDetailView

urlpatterns = [

    path('', MainListView.as_view(), name='main'),
    path('lk/', LkListView.as_view(), name='lk'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('auth/', include('authapp.urls', namespace='auth')),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

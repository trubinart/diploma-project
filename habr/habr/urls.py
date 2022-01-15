from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
import mainapp.views as mainapp
from authapp.views import RegistrationViews

urlpatterns = [
    path('', mainapp.MainListView.as_view(), name='main'),
    path('article/<str:pk>/', mainapp.ArticleDetailView.as_view(), name='article'),
    path('registration/',RegistrationViews.as_view()),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

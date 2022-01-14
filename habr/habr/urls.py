from django.contrib import admin
from django.urls import path
import mainapp.views as mainapp
from django.conf import settings
from django.conf.urls.static import static
from authapp.views import RegistrationViews

urlpatterns = [
    path('', mainapp.MainListView.as_view(), name='main'),
    path('article/', mainapp.ArticleListView.as_view(), name='article'),
    path('admin/', admin.site.urls),
    path('registration/', RegistrationViews.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

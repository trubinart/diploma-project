from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import MainListView, LkListView, ArticleDetailView
from authapp.views import RegistrationViews

urlpatterns = [
    # <<<<<<< HEAD
    #     path('', mainapp.MainListView.as_view(), name='main'),
    #     path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    #     path('lk/', mainapp.LkListView.as_view(), name='lk'),
    #     path('registration/', RegistrationViews.as_view()),
    # =======

    path('', MainListView.as_view(), name='main'),
    path('lk/', LkListView.as_view(), name='lk'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('registration/', RegistrationViews.as_view(), name='registration'),
    # >>>>>>> ac44b0f359aa9e29fde173060d747fe2232b889d
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainapp.views import MainListView, ArticleDetailView
from authapp.views import UserRegistrationView, LkListView #, LkListEditView

urlpatterns = [

    path('', MainListView.as_view(), name='main'),
    path('lk/', LkListView.as_view(), name='lk'),
    # path('lk/<user:pk>', LkListEditView.as_view(), name='lk_edit'),
    path('article/<str:pk>/', ArticleDetailView.as_view(), name='article'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

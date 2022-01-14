from django.views.generic import ListView, DetailView

from mainapp.models import Article
from authapp.models import User


class MainListView(ListView):
    """Класс для вывода списка «Хабров» на главной """
    template_name = 'mainapp/index.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Главная'
        context['title'] = title
        return context


class ArticleDetailView(DetailView):
    """Класс для вывода страницы статьи и подборок «Хабров» """
    template_name = 'mainapp/article_page.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Статья'
        context['title'] = title
        print(context)
        return context

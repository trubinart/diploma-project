from django.shortcuts import render

# Тестова ф-я для отдачи главной
# def main(request):
#     content = {
#         'title': 'главная'
#     }
#     return render(request, 'mainapp/index.html', content)
from django.views.generic import ListView


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

from django.shortcuts import render
from django.views.generic import ListView


class RegistrationViews(ListView):
    """Класс для вывода страницы статьи и подборок «Хабров» """
    template_name = 'authapp/registration.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Регистрация'
        context['title'] = title
        return context
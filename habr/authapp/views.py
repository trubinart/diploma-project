from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from authapp.forms import UserRegisterForm
from authapp.models import User


class UserRegisterView(CreateView):
    model = User
    template_name = 'authapp/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('main')
    #fields = ['username', 'email', 'password']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Регистрация'
        context['title'] = title
        return context

    def form_valid(self, form):
        form.instance.username = self.request.username
        form.instance.email = self.request.email
        form.instance.password = self.request.password
        form.save()
        return super(UserRegisterView, self).form_valid(form)


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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authapp.forms import UserRegisterForm, UserLoginForm
from authapp.models import User


class UserRegistrationView(CreateView):
    model = User
    template_name = 'authapp/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Регистрация'
        context['title'] = title
        return context


class UserLoginView(LoginView):
    template_name = 'authapp/authorization.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('main')

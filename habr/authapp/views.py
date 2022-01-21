from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from authapp.forms import UserRegisterForm, UserProfileForm
from authapp.models import User, UserProfile


class UserRegistrationView(CreateView):
    model = User
    template_name = 'authapp/registration.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Регистрация'
        context['title'] = title
        return context


# class LkListView(ListView):
class LkListView(ListView):
    """Класс для вывода страницы ЛК """
    model = UserProfile
    template_name = 'authapp/user_lk.html'
    # form_class = UserProfileForm
    success_url = reverse_lazy('main')

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Личный кабинет'
        # name =
        context['title'] = title
        # context['name'] = name
        # context['name'] = UserProfileEditForm.name

        return context

# class LkListEditView(UpdateView):
#     """Класс для вывода страницы ЛК """
#     model = UserProfile
#     template_name = 'authapp/user_lk.html'
#     form_class = UserProfileEditForm
#     success_url = reverse_lazy('lk')
#
#     def get_queryset(self):
#         # Заглушка на время отсутствия модели...
#         return
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         title = 'Личный кабинет'
#         # name =
#         context['title'] = title
#         # context['name'] = name
#         # context['name'] = UserProfileEditForm.name
#
#         return context

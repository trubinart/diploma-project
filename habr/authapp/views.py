from django.urls import reverse_lazy
from django.views.generic import CreateView

from authapp.forms import UserRegisterForm
from authapp.models import User


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

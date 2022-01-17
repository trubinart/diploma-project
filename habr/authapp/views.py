# from django.shortcuts import render
from django.views.generic import ListView

from mainapp.models import ArticleCategories


# from django.shortcuts import render, HttpResponseRedirect
# from django.urls import reverse
# from authapp.forms import UserRegisterForm
#
#
# def register(request):
#     title = 'Регистрация'
#
#     if request.method == 'POST':
#         register_form = UserRegisterForm(request.POST, request.FILES)
#
#         if register_form.is_valid():
#             register_form.save()
#             return HttpResponseRedirect(reverse('auth:login'))
#
#     else:
#         register_form = UserRegisterForm()
#
#     content = {'title': title, 'register_form': register_form}
#
#     return render(request, 'authapp/register.html', content)

class RegistrationViews(ListView):
    """Класс для вывода страницы статьи и подборок «Хабров» """
    template_name = 'authapp/registration.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['categories_list'] = ArticleCategories.objects.all()
        return context

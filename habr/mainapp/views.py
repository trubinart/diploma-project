from django.urls import reverse
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import ListView, DetailView, View, UpdateView
from uuid import UUID

from authapp.models import User, UserProfile
from mainapp.models import Article, ArticleCategories
from mainapp.forms import CreationCommentForm, UserProfileEditForm, UserProfileForm

"""обозначение списка категорий для вывода в меню во разных view"""
category_list = ArticleCategories.objects.all()


class MainListView(ListView):
    """Класс для вывода списка «Хабров» на главной """
    template_name = 'mainapp/index.html'
    paginate_by = 9
    model = Article

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'
        # добавляем в набор запросов все категории
        context['categories_list'] = category_list
        return context


class ArticleDetailView(DetailView):
    """Класс для вывода страницы статьи и подборок «Хабров» """
    template_name = 'mainapp/article_page.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Статья'
        context['title'] = title
        context['form'] = CreationCommentForm()
        context['categories_list'] = category_list
        return context


class CategoriesListView(ListView):
    """Класс для вывода списка категорий """
    template_name = 'mainapp/categories.html'
    paginate_by = 9
    model = Article

    def get_queryset(self):
        # Объявляем переменную и записываем ссылку на id категории
        categories = self.kwargs['pk']
        new_context = Article.objects.filter(categories_id=categories)
        return new_context

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        category = ArticleCategories.objects.get(id=category_id)
        context['title'] = f'Статьи по категории {category.name}'
        context['categories_list'] = category_list
        context['categories_pk'] = UUID(category_id)
        return context


class LkListView(ListView):
    # class LkEditView(UserChan):
    """Класс для вывода страницы ЛК """
    model = UserProfileForm
    # model = UserProfile
    template_name = 'mainapp/user_lk.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return UserProfile.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Личный кабинет'
        context['title'] = title
        context['form'] = UserProfileForm()
        # context['form'] = UserProfileEditForm()
        # context['name'] = UserProfile.name
        return context

# class LkListView(ListView):
class LkEditView(UpdateView):
    """Класс для вывода страницы ЛК """
    # model = UserProfileForm
    model = UserProfileEditForm
    template_name = 'mainapp/user_lk_update.html'

    # def get_queryset(self):
    #     # Заглушка на время отсутствия модели...
    #     return UserProfile.objects.filter(user=self.request.user)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     title = 'Личный кабинет'
    #     context['title'] = title
    #     # context['form'] = UserProfileForm()
    #     context['form'] = UserProfileEditForm()
    #     # context['name'] = UserProfile.name
    #     return context

    @staticmethod
    def post(request):
        title = 'Редактирование ЛК'
        if request.POST:
            # article_id = request.POST
            edit_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
            if edit_form.is_valid():
                edit_form.save()
                return HttpResponseRedirect(reverse('lk'))
        else:
            edit_form = UserProfileEditForm(instance=request.user)
            return HttpResponseRedirect(reverse('lk'))

        content = {'title': title, 'edit_form': edit_form}
        return render(request, LkEditView.template_name, content)

# class LkUpdateView(UpdateView):
#     # LkUpdateView
#     template_name = 'mainapp/user_lk.html'
#
#     def get_queryset(self, ):
#         # Заглушка на время отсутствия модели...
#
#         # return UserProfileForm.objects.filter(borrower=self.request.user.id)
#         return User.get_profile(self.fields)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         title = 'Личный кабинет'
#         context['title'] = title
#         context['form'] = UserProfileForm()
#         return context

    # @staticmethod
    # def post(request):
    #     article_id = request.POST['article_comment']
    #     # article_id = request.POST
    #     form = UserProfileForm(data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('lk'))
    #     else:
    #         form = UserProfileForm()
    #         return HttpResponseRedirect(reverse('lk'))
    pass


class CreateCommentView(View):
    """Класс для создания комментария """

    @staticmethod
    def post(request):
        article_id = request.POST['article_comment']
        form = CreationCommentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('article', kwargs={'pk': article_id}))
        else:
            return HttpResponseRedirect(reverse('article', kwargs={'pk': article_id}))


class UserArticleListView(ListView):
    """Класс для вывода списка статей автора"""
    template_name = 'mainapp/article_by_author.html'
    paginate_by = 9
    model = Article

    def get_queryset(self):
        # Объявляем переменную user и записываем ссылку на id автора
        user_id = self.kwargs['pk']
        new_context = Article.objects.filter(user=user_id)
        return new_context

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['pk']
        author = User.objects.get(id=user_id)
        context['title'] = f'Статьи автора {author.get_profile().name}'
        context['categories_list'] = category_list
        context['author'] = author
        return context

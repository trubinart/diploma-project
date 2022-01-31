from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView
from django.shortcuts import HttpResponseRedirect

from django.urls import reverse
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic import ListView, DetailView, View, UpdateView
from uuid import UUID

from authapp.forms import UserRegisterForm
from mainapp.forms import ArticleEditForm, CreationCommentForm
from authapp.models import User, UserProfile
from mainapp.models import Article, ArticleCategories
from mainapp.forms import CreationCommentForm, SearchForm
from mainapp.forms import CreationCommentForm, UserProfileEditForm, UserProfileForm

"""обозначение списка категорий для вывода в меню во разных view"""
category_list = ArticleCategories.objects.all()

"""обозначение формы поиска для вывода в меню во разных view"""
search_form = SearchForm()


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
        context['search_form'] = search_form
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
        context['search_form'] = search_form
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
        context['search_form'] = search_form
        return context


class LkListView(ListView):
    # class LkEditView(UserChan):
    """Класс для вывода страницы ЛК """
    template_name = 'mainapp/user_lk.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Личный кабинет'
        context['title'] = title
        context['categories_list'] = category_list
        return context


class CreateArticle(CreateView):
    """Класс для создания статьи"""
    model = Article
    template_name = 'mainapp/updateArticle.html'
    form_class = ArticleEditForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Добавление статьи'
        context['title'] = title
        context['categories_list'] = category_list
        return context


class UpdateArticle(UpdateView):
    """Класс для создания статьи"""
    model = Article
    template_name = 'mainapp/updateArticle.html'
    form_class = ArticleEditForm

    # success_url = reverse_lazy('article')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Редактирование статьи'
        context['title'] = title
        context['categories_list'] = category_list
        return context

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('article', args=[pk])


class ProfileCreateView(CreateView):
    model = UserProfile
    template_name = 'mainapp/updateProfile.html'
    # form_class = UserProfileEditForm
    form_class = UserProfileForm
    success_url = reverse_lazy('lk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Заполнение профиля'
        context['title'] = title
        context['categories_list'] = category_list
        return context


class ProfileEditView(UpdateView):
    model = UserProfile
    template_name = 'mainapp/updateProfile.html'
    form_class = UserProfileEditForm
    success_url = reverse_lazy('lk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Редактирование профиля'
        context['title'] = title
        context['categories_list'] = category_list
        return context


# class LkListView(ListView):
class LkEditView(UpdateView):
    """Класс для вывода страницы ЛК """
    model = UserProfileEditForm
    template_name = 'mainapp/user_lk_update.html'

    @staticmethod
    def post(request):
        title = 'Редактирование ЛК'
        if request.POST:
            edit_user_form = UserRegisterForm(request.POST, request.FILES, instance=request.user)
            profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
            if edit_user_form.is_valid() and profile_form.is_valid():
                edit_user_form.save()
                profile_form.save()
                return HttpResponseRedirect(reverse('lk'))
        else:
            edit_user_form = UserRegisterForm(instance=request.user)
            profile_form = UserProfileEditForm(instance=request.user.userprofile)
            return HttpResponseRedirect(reverse('lk'))

        content = {'title': title, 'edit_user_form': edit_user_form, 'profile_form': profile_form}
        return render(request, LkEditView.template_name, content)


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
        try:
            context['title'] = f'Статьи автора {author.get_profile().name}'
        except:
            context['title'] = f'Статьи автора {author.username}'
        context['categories_list'] = category_list
        context['author'] = author
        context['search_form'] = search_form
        return context


class MyArticleListView(ListView):
    """Класс для вывода списка статей автора"""
    template_name = 'mainapp/myArticles.html'
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
        context['categories_list'] = category_list
        context['title'] = f'Мои статьи'
        return context


# TODO убрать пагинацию на странице с результатами поиска
class SearchView(ListView):
    template_name = 'mainapp/search.html'
    paginate_by = 9
    model = Article

    def get_queryset(self):
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query_string = form.cleaned_data['query']
            search_results = Article.objects.search(query=query_string)
            return search_results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = search_form
        context['categories_list'] = category_list
        context['title'] = 'Поиск по сайту'
        context['query'] = self.request.GET['query']
        return context

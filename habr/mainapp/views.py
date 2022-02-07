from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.urls import reverse
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, CreateView, View, RedirectView, UpdateView
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404

from uuid import UUID

from authapp.forms import UserRegisterForm
from mainapp.forms import UserProfileEditForm, UserProfileForm
from mainapp.forms import ArticleEditForm, CreationCommentForm, SearchForm
from authapp.models import User, UserProfile
from mainapp.models import Article, ArticleCategories, ArticleComment

"""обозначение списка категорий для вывода в меню во разных view"""
category_list = ArticleCategories.objects.all()

"""обозначение формы поиска для вывода в меню во разных view"""
search_form = SearchForm()

"""метод получения параметра сортировки"""


def get_sort_from_request(self):
    try:
        sort = self.request.GET['sort']
        return sort
    except Exception:
        return None


class MainListView(ListView):
    """Класс для вывода списка «Хабров» на главной """
    template_name = 'mainapp/index.html'
    paginate_by = 9
    model = Article

    def get_sort_from_request(self):
        return get_sort_from_request(self)

    def get_queryset(self):
        sort = self.get_sort_from_request()

        if sort == 'date_reverse':
            return Article.objects.all().reverse()
        elif sort == 'rating':
            return Article.objects.order_by('article_rating__rating').reverse()
        elif sort == 'rating_reverse':
            return Article.objects.order_by('article_rating__rating')
        else:
            return Article.objects.all()

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная'

        # добавляем в набор запросов все категории
        context['categories_list'] = category_list
        context['search_form'] = search_form

        # добавляем сортировку
        sort = self.get_sort_from_request()
        context['sort'] = sort
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

    def get_sort_from_request(self):
        return get_sort_from_request(self)

    def get_queryset(self):
        sort = self.get_sort_from_request()
        # Объявляем переменную и записываем ссылку на id категории
        categories = self.kwargs['pk']

        if sort == 'date_reverse':
            return Article.objects.filter(categories_id=categories).reverse()
        elif sort == 'rating':
            return Article.objects.filter(categories_id=categories).order_by('article_rating__rating').reverse()
        elif sort == 'rating_reverse':
            return Article.objects.filter(categories_id=categories).order_by('article_rating__rating')
        else:
            return Article.objects.filter(categories_id=categories)

    def get_context_data(self, **kwargs):
        # вызов базовой реализации для получения контекста
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['pk']
        category = ArticleCategories.objects.get(id=category_id)
        context['title'] = f'Статьи по категории {category.name}'
        context['categories_list'] = category_list
        context['categories_pk'] = UUID(category_id)
        context['category_name'] = category.name
        context['search_form'] = search_form
        # добавляем сортировку
        sort = self.get_sort_from_request()
        context['sort'] = sort
        return context


class LkListView(ListView):
    # class LkEditView(UserChan):
    """Класс для вывода страницы ЛК """
    template_name = 'mainapp/user_lk.html'
    LOGIN_URL = 'main'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Личный кабинет'
        context['title'] = title
        context['categories_list'] = category_list
        return context

    @method_decorator(user_passes_test(lambda u: u.is_active))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Редактирование статьи'
        context['title'] = title
        context['categories_list'] = category_list
        return context

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('article', args=[pk])

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UpdateArticle, self).dispatch(*args, **kwargs)


class ProfileCreateView(CreateView):
    model = UserProfile
    template_name = 'mainapp/updateProfile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('lk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Заполнение профиля'
        context['title'] = title
        context['categories_list'] = category_list
        return context

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileCreateView, self).dispatch(*args, **kwargs)


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

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(*args, **kwargs)


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

    def get_sort_from_request(self):
        return get_sort_from_request(self)

    def get_queryset(self):
        sort = self.get_sort_from_request()
        # Объявляем переменную user и записываем ссылку на id автора
        user_id = self.kwargs['pk']

        if sort == 'date_reverse':
            return Article.objects.filter(user=user_id).reverse()
        elif sort == 'rating':
            return Article.objects.filter(user=user_id).order_by('article_rating__rating').reverse()
        elif sort == 'rating_reverse':
            return Article.objects.filter(user=user_id).order_by('article_rating__rating')
        else:
            return Article.objects.filter(user=user_id)

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
        # добавляем сортировку
        sort = self.get_sort_from_request()
        context['sort'] = sort
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


class SearchView(ListView):
    template_name = 'mainapp/search.html'
    paginate_by = 9
    model = Article

    def get_sort_from_request(self):
        return get_sort_from_request(self)

    def get_queryset(self):
        sort = self.get_sort_from_request()
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query_string = form.cleaned_data['query']

            if sort == 'date_reverse':
                return Article.objects.search(query=query_string).reverse()
            elif sort == 'rating':
                return Article.objects.search(query=query_string).order_by('article_rating__rating').reverse()
            elif sort == 'rating_reverse':
                return Article.objects.search(query=query_string).order_by('article_rating__rating')
            else:
                return Article.objects.search(query=query_string)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = search_form
        context['categories_list'] = category_list
        context['title'] = 'Поиск по сайту'
        context['query'] = self.request.GET['query']
        # добавляем сортировку
        sort = self.get_sort_from_request()
        context['sort'] = sort
        return context


class ArticleLikeRedirectView(RedirectView):
    """Класс для постановки лайка статье"""

    def get_redirect_url(self, *args, **kwargs):
        article_id = self.kwargs.get('pk')
        obj_article = get_object_or_404(Article, id=article_id)
        url_article = obj_article.get_absolute_url()
        user = self.request.user

        if user.is_authenticated:
            if user in obj_article.likes.all():
                obj_article.likes.remove(user)
            else:
                obj_article.likes.add(user)
        else:
            pass
        return url_article


class CommentLikeRedirectView(RedirectView):
    """Класс для постановки лайка комменту"""

    def get_redirect_url(self, *args, **kwargs):
        obj_article = get_object_or_404(Article, id=self.kwargs['pk'])
        url_article = obj_article.get_absolute_url()
        user = self.request.user

        obj_comment = get_object_or_404(ArticleComment, id=self.kwargs['id'])
        if user.is_authenticated:
            if user in obj_comment.likes.all():
                obj_comment.likes.remove(user)
            else:
                obj_comment.likes.add(user)
        else:
            pass
        return url_article


class AuthorStarRedirectView(RedirectView):
    """Класс для постановки звезды(лайка) автору статьи"""

    def get_redirect_url(self, *args, **kwargs):
        obj_article = get_object_or_404(Article, id=self.kwargs['pk'])
        url_article = obj_article.get_absolute_url()
        user = self.request.user

        obj_userprofile = get_object_or_404(UserProfile, user_id=obj_article.user_id)
        if user.is_authenticated:
            if user in obj_userprofile.stars.all():
                obj_userprofile.stars.remove(user)
            else:
                obj_userprofile.stars.add(user)
        else:
            pass
        return url_article


class AuthorArticleStarRedirectView(RedirectView):
    """Класс для постановки звезды(лайка) автору статьи"""

    def get_redirect_url(self, *args, **kwargs):
        user_id = self.kwargs['pk']
        obj_author = get_object_or_404(User, id=user_id)
        url_author_article = obj_author.get_absolute_url()
        user = self.request.user

        obj_userprofile = get_object_or_404(UserProfile, user_id=obj_author.id)
        if user.is_authenticated:
            if user in obj_userprofile.stars.all():
                obj_userprofile.stars.remove(user)
            else:
                obj_userprofile.stars.add(user)
        else:
            pass
        return url_author_article

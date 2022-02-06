from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, View, RedirectView, UpdateView
from django.shortcuts import HttpResponseRedirect, render, get_object_or_404
from uuid import UUID

from authapp.forms import UserRegisterForm
from mainapp.forms import UserProfileEditForm, UserProfileForm
from mainapp.forms import ArticleEditForm, CreationCommentForm, SearchForm
from authapp.models import User, UserProfile
from mainapp.models import Article, ArticleCategories, ArticleComment

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

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
        if not sort:
            return Article.objects.all()
        elif sort == 'date_reverse':
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

        if not sort:
            return Article.objects.filter(categories_id=categories)
        elif sort == 'date_reverse':
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
        context['search_form'] = search_form
        # добавляем сортировку
        sort = self.get_sort_from_request()
        context['sort'] = sort
        return context


class LkListView(ListView):
    # class LkEditView(UserChan):
    """Класс для вывода страницы ЛК """
    # model = UserProfileForm
    # model = UserProfile
    template_name = 'mainapp/user_lk.html'

    def get_queryset(self):
        # Заглушка на время отсутствия модели...
        # UserProfile.objects.filter(user=self.request.user)
        return

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Личный кабинет'
        context['title'] = title
        # context['form'] = UserProfileForm()
        # context['form'] = UserProfileEditForm()
        # context['name'] = UserProfile.name
        context['categories_list'] = category_list
        return context


class CreateArticle(CreateView):
    """Класс для создания статьи"""
    model = Article
    template_name = 'mainapp/createArticle.html'
    form_class = ArticleEditForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Добавление статьи'
        context['title'] = title
        context['categories_list'] = category_list
        return context


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
    # form_class = UserProfileForm
    # form_class2 = UserRegisterForm
    success_url = reverse_lazy('lk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Редактирование профиля'
        context['title'] = title
        # context['user'] = User.objects.all()
        context['categories_list'] = category_list
        # edit_form = UserProfileForm(instance=request.user)
        # profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
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
            # edit_user_form = UserProfileEditForm(request.POST, request.FILES, instance=request.user)
            edit_user_form = UserRegisterForm(request.POST, request.FILES, instance=request.user)
            profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)
            if edit_user_form.is_valid() and profile_form.is_valid():
                edit_user_form.save()
                profile_form.save()
                # messages.success(request, _('Your profile was successfully updated!'))
                return HttpResponseRedirect(reverse('lk'))
        else:
            edit_user_form = UserRegisterForm(instance=request.user)
            profile_form = UserProfileEditForm(instance=request.user.userprofile)
            return HttpResponseRedirect(reverse('lk'))

        content = {'title': title, 'edit_user_form': edit_user_form, 'profile_form': profile_form}
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

    def get_sort_from_request(self):
        return get_sort_from_request(self)

    def get_queryset(self):
        sort = self.get_sort_from_request()
        # Объявляем переменную user и записываем ссылку на id автора
        user_id = self.kwargs['pk']

        if not sort:
            return Article.objects.filter(user=user_id)
        elif sort == 'date_reverse':
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

            if not sort:
                return Article.objects.search(query=query_string)
            elif sort == 'date_reverse':
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

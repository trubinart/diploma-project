from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, View, RedirectView
from django.shortcuts import HttpResponseRedirect, get_object_or_404

from uuid import UUID

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

    #TODO на страницах вывода статей по категориям лайки не отображаются
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
    template_name = 'mainapp/createArticle.html'
    form_class = ArticleEditForm
    success_url = reverse_lazy('main')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        title = 'Добавление статьи'
        context['title'] = title
        context['categories_list'] = category_list
        return context


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

    # TODO на страницах вывода статей по автору лайки не отображаются
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
            return reverse_lazy('auth:login')
        return url_article


class ArticleLikeRedirectAPIView(APIView):
    """Класс для постановки лайка статье через API REST_framework"""

    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk=None):
        obj = get_object_or_404(Article, pk=pk)
        #TODO переменную нигде не используешь
        url_ = obj.get_absolute_url()
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated:
            if user in obj.likes.all():
                liked = False
                obj.likes.remove(user)
            else:
                liked = True
                obj.likes.add(user)
            updated = True

        data = {
            "updated": updated,
            "liked": liked
        }
        return Response(data)


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
            return reverse_lazy('auth:login')
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
            return reverse_lazy('auth:login')
        return url_article

from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView

# from .models import *
from .forms import *


# menu = ['О сайте', 'Добавить статью', 'Обратная связь', 'Войти']

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Главная страница'
        context['cat_selected'] = 0
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


# def index(request):
#     posts = Women.objects.all()
#     context = {
#         'posts': posts,
#         'cat_selected': 0,
#         'title': 'Главная страница'
#     }
#     return render(request, 'women/index.html', context=context)


class WomenCategory(ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        context['cat_selected'] = self.kwargs['cat_slug']
        return context

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


# def show_category(request, cat_slug):
#     posts = Women.objects.filter(cat__slug=cat_slug)
#     if len(posts) == 0:
#         raise Http404()
#     context = {
#         'posts': posts,
#         'cat_selected': cat_slug,
#         'title': 'Отображение по рубрикам'
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте'})


def addpage(request):
    if request.POST:
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            # print(form.cleaned_data)
            # Women.objects.create(**form.cleaned_data)
            form.save()
            return redirect('home')

    else:
        form = AddPostForm()
    return render(request, 'women/add_page.html', {'form': form, 'title': 'Добавление статьи'})


def contact(request):
    return HttpResponse('Обратная связь')


def login(request):
    return HttpResponse('Авторизация')


class WomenPost(DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = str(context['post'].cat) + ' - ' + context['post'].title
        context['cat_selected'] = str(context['post'].cat.slug)
        return context


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'cat_selected': post.cat_id,
#         'title': post.title
#     }
#     return render(request, 'women/post.html', context)


def categories(request, catid):
    if request.GET:
        print(request.GET)
    return HttpResponse(f'<h1>Статьи по категориям</h1><p>{catid}</p>')


def archive(request, year):
    if int(year) > 2022:
        # raise Http404()
        return redirect('home', permanent=True)
    return HttpResponse(f'<h1>Архив по годам</h1><p>{year}</p>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
